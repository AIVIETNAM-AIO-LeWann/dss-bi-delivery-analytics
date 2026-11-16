"""Generate the team's native PBIP/PBIR report from one maintainable definition."""
from pathlib import Path
import json
import uuid
import hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dashboards/powerbi'
REPORT = OUT/'Delivery.Report'
MODEL = OUT/'Delivery.SemanticModel'
SCHEMA = 'https://developer.microsoft.com/json-schemas/fabric/'


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')


def literal(value):
    if isinstance(value, bool):
        text = str(value).lower()
    elif isinstance(value, (int, float)):
        text = str(value)+'D'
    else:
        text = "'"+str(value).replace("'", "''")+"'"
    return {'expr': {'Literal': {'Value': text}}}


def color(value):
    return {'solid': {'color': literal(value)}}


TABLES = {
    'Orders': ('orders.csv', {'order_id':'string','order_date':'dateTime','year_month':'string',
        'shipping_mode':'string','market':'string','order_region':'string','customer_segment':'string',
        'shipping_days_scheduled':'int64','shipping_days_actual':'int64','late_delivery_risk':'int64',
        'partition':'string','P_Late':'double','duration_mismatch_flag':'int64'}),
    'PromiseScenarios': ('promise_scenarios.csv', {'order_id':'string','policy_id':'string','proposed_days':'int64',
        'exceed_proposed':'int64','fallback':'int64','added_days':'int64'}),
    'Policies': ('policies.csv', {'policy_id':'string','policy_label':'string','sort_order':'int64'}),
    'RouteCases': ('route_cases.csv', {'case_id':'string','instance':'string','scenario':'string','method':'string',
        'max_vehicles':'int64','capacity':'int64','status':'string','vehicles_used':'int64','distance_units':'double'}),
    'RouteStops': ('route_stops.csv', {'sequence':'int64','node':'int64','x':'double','y':'double','vehicle':'string','case_id':'string','stop_key':'string'}),
    'ModelMetrics': ('model_metrics.csv', {'model':'string','partition':'string','n':'int64','late_count':'int64',
        'late_rate':'double','roc_auc':'double','average_precision':'double','log_loss':'double','brier':'double',
        'accuracy':'double','precision':'double','recall':'double','f1':'double','threshold':'double',
        'tn':'int64','fp':'int64','fn':'int64','tp':'int64'}),
}

MEASURES = {
    'Orders': [
        ('Số đơn', 'COALESCE(COUNTROWS(Orders), 0)', '#,0'),
        ('Số đơn trễ', 'COALESCE(SUM(Orders[late_delivery_risk]), 0)', '#,0'),
        ('Tỷ lệ trễ', 'DIVIDE([Số đơn trễ], [Số đơn])', '0.00%'),
        ('Cam kết TB', 'AVERAGE(Orders[shipping_days_scheduled])', '0.00" ngày"'),
        ('Thực tế TB', 'AVERAGE(Orders[shipping_days_actual])', '0.00" ngày"'),
        ('Đơn test', 'CALCULATE([Số đơn], Orders[partition] = "test")', '#,0'),
        ('Ngưỡng cảnh báo', 'SELECTEDVALUE(RiskThreshold[Value], 0.5)', '0.00'),
        ('Cảnh báo', 'VAR t = [Ngưỡng cảnh báo] RETURN CALCULATE([Đơn test], KEEPFILTERS(Orders[P_Late] >= t), KEEPFILTERS(NOT ISBLANK(Orders[P_Late])))', '#,0'),
        ('Cảnh báo đúng', 'CALCULATE([Cảnh báo], Orders[late_delivery_risk] = 1)', '#,0'),
        ('Đơn trễ test', 'CALCULATE([Số đơn trễ], Orders[partition] = "test")', '#,0'),
        ('Precision theo ngưỡng', 'DIVIDE([Cảnh báo đúng], [Cảnh báo])', '0.00%'),
        ('Recall theo ngưỡng', 'DIVIDE([Cảnh báo đúng], [Đơn trễ test])', '0.00%'),
        ('Bỏ sót', '[Đơn trễ test] - [Cảnh báo đúng]', '#,0'),
        ('P_Late TB test', 'CALCULATE(AVERAGE(Orders[P_Late]), Orders[partition] = "test")', '0.00%'),
    ],
    'PromiseScenarios': [
        ('Chính sách đang xem', 'SELECTEDVALUE(Policies[policy_label], "+1 ngày, giữ Same Day")', None),
        ('Đơn kịch bản', 'VAR p = SELECTEDVALUE(Policies[policy_id], "bounded_plus1_keep_same_day") RETURN CALCULATE(COUNTROWS(PromiseScenarios), KEEPFILTERS(Policies[policy_id] = p))', '#,0'),
        ('Vượt hẹn tính lại', 'VAR p = SELECTEDVALUE(Policies[policy_id], "bounded_plus1_keep_same_day") RETURN DIVIDE(CALCULATE(SUM(PromiseScenarios[exceed_proposed]), KEEPFILTERS(Policies[policy_id] = p)), [Đơn kịch bản])', '0.00%'),
        ('Cam kết mới TB', 'VAR p = SELECTEDVALUE(Policies[policy_id], "bounded_plus1_keep_same_day") RETURN CALCULATE(AVERAGE(PromiseScenarios[proposed_days]), KEEPFILTERS(Policies[policy_id] = p))', '0.00" ngày"'),
        ('Tăng cam kết TB', 'VAR p = SELECTEDVALUE(Policies[policy_id], "bounded_plus1_keep_same_day") RETURN CALCULATE(AVERAGE(PromiseScenarios[added_days]), KEEPFILTERS(Policies[policy_id] = p))', '0.00" ngày"'),
        ('Trễ hiện trạng test', 'DIVIDE([Đơn trễ test], [Đơn test])', '0.00%'),
        ('Giảm vượt hẹn (điểm %)', 'IF([Đơn kịch bản] > 0, ([Trễ hiện trạng test] - [Vượt hẹn tính lại]) * 100)', '0.00" điểm %"'),
    ],
    'RouteCases': [
        ('Quãng đường benchmark', 'IF(HASONEVALUE(RouteCases[case_id]) && SELECTEDVALUE(RouteCases[status]) = "feasible", SELECTEDVALUE(RouteCases[distance_units]))', '0.00'),
        ('Số xe sử dụng', 'IF(HASONEVALUE(RouteCases[case_id]) && SELECTEDVALUE(RouteCases[status]) = "feasible", SELECTEDVALUE(RouteCases[vehicles_used]))', '#,0'),
        ('Km mô phỏng', '[Quãng đường benchmark] * SELECTEDVALUE(KmPerUnit[Value], 1)', '0.00'),
        ('Nhiên liệu mô phỏng', '[Km mô phỏng] * SELECTEDVALUE(FuelConsumption[Value], 10) / 100 * SELECTEDVALUE(FuelPrice[Value], 22000)', '#,0'),
        ('Trạng thái tuyến', 'IF(HASONEVALUE(RouteCases[case_id]), IF(SELECTEDVALUE(RouteCases[status]) = "feasible", "Có tuyến khả thi — chưa chứng minh tối ưu", "Chưa tìm được lời giải — không quy về 0"), "Chọn đúng một case_id để xem tuyến và chi phí")', None),
    ],
    'RouteStops': [
        ('Node tuyến', 'SELECTEDVALUE(RouteStops[node])', '#,0'),
        ('Thứ tự dừng', 'SELECTEDVALUE(RouteStops[sequence])', '#,0'),
        ('Tọa độ X', 'IF(HASONEVALUE(RouteCases[case_id]), AVERAGE(RouteStops[x]))', '0.0'),
        ('Tọa độ Y', 'IF(HASONEVALUE(RouteCases[case_id]), AVERAGE(RouteStops[y]))', '0.0'),
    ],
    'ModelMetrics': [
        ('AUC baseline test', 'CALCULATE(MAX(ModelMetrics[roc_auc]), ModelMetrics[model] = "mode_baseline", ModelMetrics[partition] = "test")', '0.000'),
        ('Log loss baseline test', 'CALCULATE(MAX(ModelMetrics[log_loss]), ModelMetrics[model] = "mode_baseline", ModelMetrics[partition] = "test")', '0.000'),
    ],
}


def import_table(name, filename, columns):
    mtypes = {'string':'type text','int64':'Int64.Type','double':'type number','dateTime':'type date'}
    types = ', '.join('{"'+key+'", '+mtypes[value]+'}' for key,value in columns.items())
    expression = [
        'let',
        f'    Source = Csv.Document(File.Contents(RepoRoot & "/data/dashboard/{filename}"), [Delimiter=",", Columns={len(columns)}, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
        '    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '    EmptyAsNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),',
        f'    Typed = Table.TransformColumnTypes(EmptyAsNull, {{{types}}}, "en-US")',
        'in', '    Typed']
    table = {'name':name, 'lineageTag':str(uuid.uuid5(uuid.NAMESPACE_URL, 'delivery/'+name)),
        'columns':[{'name':key, 'dataType':value, 'sourceColumn':key, 'summarizeBy':'none',
                    **({'formatString':'0.00%'} if key == 'P_Late' else {}),
                    **({'formatString':'yyyy-MM-dd'} if key == 'order_date' else {})} for key,value in columns.items()],
        'partitions':[{'name':name, 'mode':'import', 'source':{'type':'m','expression':expression}}]}
    if name == 'ModelMetrics':
        for column in table['columns']:
            if column['dataType'] == 'double':
                column['formatString'] = '0.000'
    if name == 'Policies':
        next(c for c in table['columns'] if c['name']=='policy_label')['sortByColumn'] = 'sort_order'
    return table


def model():
    tables = [import_table(name,*spec) for name,spec in TABLES.items()]
    for name,values in {'RiskThreshold':('GENERATESERIES(CURRENCY(0), CURRENCY(1), CURRENCY(0.01))','decimal'),
                        'KmPerUnit':('GENERATESERIES(0.5, 1.5, 0.1)','double'),
                        'FuelConsumption':('GENERATESERIES(8, 14, 1)','double'),
                        'FuelPrice':('GENERATESERIES(18000, 26000, 1000)','int64')}.items():
        tables.append({'name':name,'columns':[{'name':'Value','dataType':values[1], 'type':'calculatedTableColumn', 'sourceColumn':'[Value]','summarizeBy':'none'}],
            'partitions':[{'name':name,'mode':'import','source':{'type':'calculated','expression':values[0]}}]})
    for table in tables:
        if table['name'] in MEASURES:
            table['measures'] = [{'name':name,'expression':expression, **({'formatString':fmt} if fmt else {})} for name,expression,fmt in MEASURES[table['name']]]
    relationships = []
    for many,column,one,key in [('PromiseScenarios','order_id','Orders','order_id'),('PromiseScenarios','policy_id','Policies','policy_id'),('RouteStops','case_id','RouteCases','case_id')]:
        relationships.append({'name':f'{many}_{column}_{one}','fromTable':many,'fromColumn':column,'toTable':one,'toColumn':key,
                              'fromCardinality':'many','toCardinality':'one','crossFilteringBehavior':'oneDirection'})
    write(MODEL/'definition.pbism',{'$schema':SCHEMA+'item/semanticModel/definitionProperties/1.0.0/schema.json','version':'1.0','settings':{}})
    write(MODEL/'model.bim',{'name':'Delivery','compatibilityLevel':1567,'model':{'culture':'en-US','defaultPowerBIDataSourceVersion':'powerBI_V3',
        'sourceQueryCulture':'en-US','expressions':[{'name':'RepoRoot','kind':'m','expression':json.dumps(ROOT.as_posix())+' meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'}],
        'tables':tables,'relationships':relationships,'annotations':[{'name':'PBI_QueryOrder','value':json.dumps(list(TABLES)+['RepoRoot'])}]}})


def field(table, prop, measure=False, display=None):
    labels = {'shipping_mode':'Phương thức','model':'Mô hình','partition':'Tập',
        'roc_auc':'ROC-AUC','average_precision':'AP','log_loss':'Log loss','brier':'Brier',
        'policy_label':'Chính sách','instance':'Bộ mẫu','scenario':'Cấu hình','method':'Phương pháp',
        'max_vehicles':'Giới hạn xe','capacity':'Sức chở','status':'Trạng thái','vehicles_used':'Xe dùng',
        'distance_units':'Quãng đường','vehicle':'Xe','sequence':'Thứ tự','node':'Điểm dừng','case_id':'Case'}
    display = display or labels.get(prop)
    return {'field':{'Measure' if measure else 'Column':{'Expression':{'SourceRef':{'Entity':table}}, 'Property':prop}},
            'queryRef':f'{table}.{prop}', 'nativeQueryRef':prop, **({'displayName':display} if display else {})}


class Page:
    def __init__(self,name,title,note):
        name=hashlib.sha256(name.encode()).hexdigest()[:20]
        self.path=REPORT/'definition/pages'/name
        self.count=0
        write(self.path/'page.json',{'$schema':SCHEMA+'item/report/definition/page/1.4.0/schema.json','name':name,'displayName':title,
            'displayOption':'FitToPage','height':960,'width':1440,
            'objects':{'background':[{'properties':{'color':color('#F1F5F9'),'transparency':literal(0)}}]}})
        self.text(title,32,8,1376,64,22,'#0F172A')
        self.text(note,32,76,1376,44,11,'#475569')

    def visual(self,kind,title,x,y,w,h,roles=None,objects=None,subtitle=None):
        self.count+=1
        name=hashlib.sha256((self.path.name+str(self.count)).encode()).hexdigest()[:20]
        v={'visualType':kind,'drillFilterOtherVisuals':True,
           'visualContainerObjects':{'title':[{'properties':{'show':literal(True),'text':literal(title),'fontSize':literal(12),'fontColor':color('#0F172A'),'fontFamily':literal('Segoe UI'),'titleWrap':literal(True)}}],
               'background':[{'properties':{'show':literal(True),'color':color('#FFFFFF'),'transparency':literal(0)}}],
               'border':[{'properties':{'show':literal(False)}}],
               'padding':[{'properties':{key:literal(8) for key in ['top','bottom','left','right']}}]}}
        if subtitle:
            v['visualContainerObjects']['subTitle']=[{'properties':{'show':literal(True),'text':literal(subtitle),'fontSize':literal(10)}}]
        if roles:
            v['query']={'queryState':{role:{'projections':projections} for role,projections in roles.items()}}
        if objects:
            v['objects']=objects
        if kind == 'tableEx':
            v.setdefault('objects', {})['grid']=[{'properties':{'textSize':literal(12),'rowPadding':literal(5)}}]
        if kind == 'scatterChart':
            v.setdefault('objects', {})['bubbles']=[{'properties':{'bubbleSize':literal(-15)}}]
        if kind == 'lineChart':
            v.setdefault('objects', {})['valueAxis']=[{'properties':{'start':literal(0),'end':literal(1)}}]
            v['objects']['categoryAxis']=[{'properties':{'preferredCategoryWidth':literal(10)}}]
        write(self.path/'visuals'/name/'visual.json',{'$schema':SCHEMA+'item/report/definition/visualContainer/2.1.0/schema.json',
            'name':name,'position':{'x':x,'y':y,'z':self.count,'height':h,'width':w,'tabOrder':self.count},'visual':v})

    def text(self,text,x,y,w,h,size=12,fill='#475569'):
        self.visual('textbox','',x,y,w,h,objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':text,'textStyle':{'fontFamily':'Segoe UI','fontSize':f'{size}pt','color':fill}}]}]}}]})

    def card(self,title,table,measure,x,y,w=260):
        self.visual('card',title,x,y,w,108,{'Values':[field(table,measure,True)]},
            objects={'labels':[{'properties':{'fontSize':literal(25),'labelDisplayUnits':literal(1),'color':color('#1E40AF')}}], 'categoryLabels':[{'properties':{'show':literal(False)}}]})

    def slicer(self,title,table,column,x,y,w=260):
        objects={'data':[{'properties':{'mode':literal('Dropdown')}}],
                 'header':[{'properties':{'show':literal(False)}}],
                 'selection':[{'properties':{'singleSelect':literal(True)}}]}
        default = 'c101|base|ortools' if table == 'RouteCases' else None
        if default:
            objects['general']=[{'properties':{'filter':{'filter':{'Version':2,
                'From':[{'Name':'s','Entity':table,'Type':0}],
                'Where':[{'Condition':{'In':{
                    'Expressions':[{'Column':{'Expression':{'SourceRef':{'Source':'s'}},'Property':column}}],
                    'Values':[[{'Literal':{'Value':"'"+default+"'"}}]]}}}]}}}}]
        self.visual('slicer',title,x,y,w,80,{'Values':[field(table,column)]},objects=objects)


def report():
    write(OUT/'delivery_dashboard.pbip',{'$schema':SCHEMA+'pbip/pbipProperties/1.0.0/schema.json','version':'1.0','artifacts':[{'report':{'path':'Delivery.Report'}}],'settings':{'enableAutoRecovery':True}})
    write(REPORT/'definition.pbir',{'$schema':SCHEMA+'item/report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../Delivery.SemanticModel'}}})
    write(REPORT/'definition/version.json',{'$schema':SCHEMA+'item/report/definition/versionMetadata/1.0.0/schema.json','version':'2.0.0'})
    write(REPORT/'definition/report.json',{'$schema':SCHEMA+'item/report/definition/report/2.1.0/schema.json',
        'themeCollection':{'customTheme':{'name':'delivery_theme.json','reportVersionAtImport':'5.59','type':'RegisteredResources'}},
        'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'delivery_theme.json','path':'delivery_theme.json','type':'CustomTheme'}]}],
        'settings':{'useStylableVisualContainerHeader':True, 'exportDataMode':'AllowSummarized'}})
    write(REPORT/'StaticResources/RegisteredResources/delivery_theme.json',{'name':'delivery_theme.json','dataColors':['#1E40AF','#D97706','#0F766E','#7C3AED','#475569'],
        'background':'#FFFFFF','foreground':'#0F172A','tableAccent':'#1E40AF',
        'textClasses':{'title':{'fontFace':'Segoe UI','fontSize':13},'label':{'fontFace':'Segoe UI','fontSize':11},'callout':{'fontFace':'Segoe UI','fontSize':28}}})
    pages=[hashlib.sha256(name.encode()).hexdigest()[:20] for name in ['overview','risk','promises','routing']]
    write(REPORT/'definition/pages/pages.json',{'$schema':SCHEMA+'item/report/definition/pagesMetadata/1.0.0/schema.json','pageOrder':pages,'activePageName':pages[0]})
    p=Page('overview','01  Tổng quan giao hàng','DataCo lịch sử 2015–2018 • Mặc định 62.897 đơn không hủy • Bộ lọc chỉ áp dụng trong trang • Không phải dữ liệu DHL thực tế')
    for x,title,col in [(32,'Phương thức','shipping_mode'),(384,'Thị trường','market'),(736,'Tháng đặt hàng','year_month'),(1088,'Vùng','order_region')]:p.slicer(title,'Orders',col,x,122,320)
    for x,title,m in [(32,'Đơn trong phạm vi','Số đơn'),(314,'Tỷ lệ giao trễ','Tỷ lệ trễ'),(596,'Cam kết trung bình','Cam kết TB'),(878,'Thời gian thực tế','Thực tế TB')]:p.card(title,'Orders',m,x,214)
    p.visual('clusteredBarChart','Tỷ lệ trễ theo phương thức',32,344,660,254,{'Category':[field('Orders','shipping_mode')],'Y':[field('Orders','Tỷ lệ trễ',True)]})
    p.visual('lineChart','Xu hướng tỷ lệ trễ theo tháng',716,344,692,254,{'Category':[field('Orders','year_month')],'Y':[field('Orders','Tỷ lệ trễ',True)]})
    p.visual('clusteredBarChart','Sản lượng theo thị trường',32,622,660,250,{'Category':[field('Orders','market')],'Y':[field('Orders','Số đơn',True)]})
    p.visual('tableEx','Đối chiếu phương thức',716,622,692,250,{'Values':[field('Orders','shipping_mode'),*[field('Orders',m,True) for m in ['Số đơn','Tỷ lệ trễ','Cam kết TB','Thực tế TB']]]})
    p.text('Nhận định: phương thức/cam kết là tín hiệu mạnh trong snapshot. Mối liên hệ không chứng minh rằng đổi phương thức sẽ làm giao nhanh hơn.',32,896,1376,46)
    p=Page('risk','02  Dự báo rủi ro — chỉ tập test','13.071 đơn test, 01/07/2017–31/01/2018 • Baseline được chọn bằng log loss validation • Chỉ bốn mức xác suất theo phương thức')
    p.slicer('Ngưỡng cảnh báo (mặc định 0,50)','RiskThreshold','Value',32,122,420)
    p.slicer('Phương thức','Orders','shipping_mode',492,122,420)
    p.slicer('Vùng','Orders','order_region',952,122,456)
    for x,title,t,m in [(32,'Đơn test','Orders','Đơn test'),(314,'Cảnh báo','Orders','Cảnh báo'),(596,'Precision','Orders','Precision theo ngưỡng'),(878,'Recall','Orders','Recall theo ngưỡng')]:p.card(title,t,m,x,214)
    p.visual('clusteredBarChart','Xác suất baseline theo phương thức',32,344,660,254,{'Category':[field('Orders','shipping_mode')],'Y':[field('Orders','P_Late TB test',True)]})
    p.visual('clusteredBarChart','Cảnh báo đúng và đơn trễ bị bỏ sót',716,344,692,254,{'Category':[field('Orders','shipping_mode')],'Y':[field('Orders','Cảnh báo đúng',True),field('Orders','Bỏ sót',True)]})
    p.visual('tableEx','So sánh mô hình (toàn tập được ghi trong bảng, không đổi khi lọc vùng)',32,622,1376,250,{'Values':[field('ModelMetrics',c) for c in ['model','partition','roc_auc','average_precision','log_loss','brier']]})
    p.text('P_Late dự báo theo cam kết cũ, có điều kiện không hủy. Ngưỡng đổi chỉ thay cách cảnh báo, không thay AUC hay hiệu quả giao hàng. Không chọn lại mô hình bằng test.',32,896,1376,46)
    p=Page('promises','03  Cam kết giao — đánh đổi trên dữ liệu test','Kịch bản hồi cứu, không phải kết quả triển khai • Cam kết mới không làm thời gian giao thực tế thay đổi • Mặc định +1 ngày, giữ Same Day')
    p.slicer('Chọn chính sách','Policies','policy_label',32,122,660)
    p.slicer('Phương thức','Orders','shipping_mode',716,122,320)
    p.slicer('Vùng','Orders','order_region',1060,122,348)
    for x,title,m in [(32,'Đơn test trong kịch bản','Đơn kịch bản'),(314,'Vượt hẹn tính lại','Vượt hẹn tính lại'),(596,'Cam kết tăng trung bình','Tăng cam kết TB'),(878,'Giảm vượt hẹn','Giảm vượt hẹn (điểm %)')]:p.card(title,'PromiseScenarios',m,x,214)
    p.visual('clusteredBarChart','Hiện trạng và kịch bản theo phương thức',32,344,660,270,{'Category':[field('Orders','shipping_mode')],'Y':[field('PromiseScenarios','Trễ hiện trạng test',True),field('PromiseScenarios','Vượt hẹn tính lại',True)]})
    p.visual('tableEx','Đánh đổi giữa các chính sách (xóa bộ lọc chính sách để so sánh tất cả)',716,344,692,270,{'Values':[field('Policies','policy_label'),*[field('PromiseScenarios',m,True) for m in ['Vượt hẹn tính lại','Cam kết mới TB','Tăng cam kết TB']]]})
    p.text('Khuyến nghị 1 — Thí điểm điều chỉnh cam kết theo phương thức và theo dõi thời gian khách chờ. Phương án +1 ngày còn vượt hẹn cao ở Second Class; không áp dụng đồng loạt chỉ vì KPI toàn mẫu giảm.',32,646,660,202,16,'#1E40AF')
    p.text('Khuyến nghị 2 — Dùng cảnh báo như tín hiệu ưu tiên ban đầu. Trước khi vận hành, cần xác minh thời điểm biết biến, khả năng hủy và chi phí xử lý; đo tác động bằng thử nghiệm thay vì suy từ P_Late.',716,646,692,202,16,'#0F766E')
    p.text('Các phân vị chỉ học từ train; test dùng đối chiếu ngoài mẫu. Giảm vượt hẹn là chênh lệch điểm phần trăm, không phải % giảm thời gian giao hoặc ROI.',32,896,1376,46)
    p=Page('routing','04  Tuyến Solomon — benchmark độc lập','Solomon độc lập với DataCo • Mặc định: C101/base/OR-Tools, 1 km/đơn vị, 10 lít/100km, 22.000 VND/lít • Các quy đổi là giả định')
    p.slicer('Case: instance | cấu hình | phương pháp','RouteCases','case_id',32,122,660)
    p.slicer('Km/đơn vị (giả định)','KmPerUnit','Value',716,122,208)
    p.slicer('Lít/100km (giả định)','FuelConsumption','Value',948,122,208)
    p.slicer('VND/lít (giả định)','FuelPrice','Value',1180,122,228)
    for x,title,m in [(32,'Xe sử dụng','Số xe sử dụng'),(314,'Quãng đường benchmark','Quãng đường benchmark'),(596,'Km quy đổi (giả định)','Km mô phỏng'),(878,'Nhiên liệu giả định (VND)','Nhiên liệu mô phỏng')]:p.card(title,'RouteCases',m,x,214)
    p.visual('scatterChart','Điểm dừng theo xe — tọa độ benchmark',32,344,660,280,{'X':[field('RouteStops','Tọa độ X',True)],'Y':[field('RouteStops','Tọa độ Y',True)],'Category':[field('RouteStops','stop_key')],'Series':[field('RouteStops','vehicle')],'Tooltips':[field('RouteStops','Node tuyến',True),field('RouteStops','Thứ tự dừng',True)]})
    p.visual('tableEx','Thứ tự điểm dừng (node 0 là kho)',716,344,692,280,{'Values':[field('RouteStops',c) for c in ['case_id','vehicle','sequence','node','x','y']]})
    p.visual('tableEx','So sánh cấu hình và phương pháp',32,648,1376,184,{'Values':[field('RouteCases',c) for c in ['instance','scenario','method','max_vehicles','capacity','status','vehicles_used','distance_units']]})
    p.card('Trạng thái','RouteCases','Trạng thái tuyến',32,846,1376)


def main():
    model()
    report()
    for folder, kind in [(REPORT, 'Report'), (MODEL, 'SemanticModel')]:
        write(folder/'.platform', {'$schema':SCHEMA+'gitIntegration/platformProperties/2.0.0/schema.json',
            'metadata':{'type':kind,'displayName':'Delivery Analytics'},
            'config':{'version':'2.0','logicalId':str(uuid.uuid5(uuid.NAMESPACE_URL,'delivery/'+kind))}})
    print('Generated PBIP, semantic model, four PBIR pages and theme.')


if __name__ == '__main__':
    main()
