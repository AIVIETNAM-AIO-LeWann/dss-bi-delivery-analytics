"""Generate the team's native PBIP/PBIR report from one maintainable definition."""
from pathlib import Path
import json
import uuid
import hashlib

ROOT = Path(__file__).resolve().parents[2]
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
    'Orders': ('orders.csv', {'order_id':'string','order_date':'dateTime','year_month':'string','month_start':'dateTime',
        'shipping_mode':'string','market':'string','order_region':'string','customer_segment':'string',
        'shipping_days_scheduled':'int64','shipping_days_actual':'int64','late_delivery_risk':'int64',
        'partition':'string','P_Late':'double','duration_mismatch_flag':'int64'}),
    'PromiseScenarios': ('promise_scenarios.csv', {'order_id':'string','policy_id':'string','proposed_days':'int64',
        'exceed_proposed':'int64','fallback':'int64','added_days':'int64'}),
    'Policies': ('policies.csv', {'policy_id':'string','policy_label':'string','sort_order':'int64'}),
    'RouteCases': ('route_cases.csv', {'case_id':'string','instance':'string','scenario':'string','method':'string',
        'max_vehicles':'int64','capacity':'int64','status':'string','vehicles_used':'int64','distance_units':'double','case_label':'string','route_image':'string'}),
    'RouteStops': ('route_stops.csv', {'sequence':'int64','node':'int64','x':'double','y':'double','vehicle':'string','case_id':'string','stop_key':'string'}),
    'ModelMetrics': ('model_metrics.csv', {'model':'string','partition':'string','n':'int64','late_count':'int64',
        'late_rate':'double','roc_auc':'double','average_precision':'double','log_loss':'double','brier':'double',
        'accuracy':'double','precision':'double','recall':'double','f1':'double','threshold':'double',
        'tn':'int64','fp':'int64','fn':'int64','tp':'int64','model_label':'string'}),
}

MEASURES = {
    'Orders': [
        ('Số đơn', 'COALESCE(COUNTROWS(Orders), 0)', '#,0'),
        ('Số đơn trễ', 'COALESCE(SUM(Orders[late_delivery_risk]), 0)', '#,0'),
        ('Tỷ lệ trễ', 'DIVIDE([Số đơn trễ], [Số đơn])', '0.0%'),
        ('Cam kết TB', 'AVERAGE(Orders[shipping_days_scheduled])', '0.00" ngày"'),
        ('Thực tế TB', 'AVERAGE(Orders[shipping_days_actual])', '0.00" ngày"'),
        ('Đơn test', 'CALCULATE([Số đơn], Orders[partition] = "test")', '#,0'),
        ('Ngưỡng cảnh báo', 'SELECTEDVALUE(RiskThreshold[Value], 0.5)', '0.00'),
        ('Cảnh báo', 'VAR t = [Ngưỡng cảnh báo] RETURN CALCULATE([Đơn test], KEEPFILTERS(Orders[P_Late] >= t), KEEPFILTERS(NOT ISBLANK(Orders[P_Late])))', '#,0'),
        ('Cảnh báo đúng', 'CALCULATE([Cảnh báo], Orders[late_delivery_risk] = 1)', '#,0'),
        ('Đơn trễ test', 'CALCULATE([Số đơn trễ], Orders[partition] = "test")', '#,0'),
        ('Precision theo ngưỡng', 'DIVIDE([Cảnh báo đúng], [Cảnh báo])', '0.0%'),
        ('Recall theo ngưỡng', 'DIVIDE([Cảnh báo đúng], [Đơn trễ test])', '0.0%'),
        ('Bỏ sót', '[Đơn trễ test] - [Cảnh báo đúng]', '#,0'),
        ('P_Late TB test', 'CALCULATE(AVERAGE(Orders[P_Late]), Orders[partition] = "test")', '0.0%'),
    ],
    'PromiseScenarios': [
        ('Chính sách đang xem', 'COALESCE(SELECTEDVALUE(PolicySelector[policy_label]), "Thêm một ngày")', None),
        ('Đơn kịch bản', 'VAR p = COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day") RETURN CALCULATE(COUNTROWS(PromiseScenarios), KEEPFILTERS(Policies[policy_id] = p))', '#,0'),
        ('Vượt hẹn tính lại', 'VAR p = COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day") RETURN DIVIDE(CALCULATE(SUM(PromiseScenarios[exceed_proposed]), KEEPFILTERS(Policies[policy_id] = p)), [Đơn kịch bản])', '0.0%'),
        ('Cam kết mới TB', 'VAR p = COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day") RETURN CALCULATE(AVERAGE(PromiseScenarios[proposed_days]), KEEPFILTERS(Policies[policy_id] = p))', '0.00" ngày"'),
        ('Tăng cam kết TB', 'VAR p = COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day") RETURN CALCULATE(AVERAGE(PromiseScenarios[added_days]), KEEPFILTERS(Policies[policy_id] = p))', '0.00" ngày"'),
        ('Trễ hiện trạng test', 'DIVIDE([Đơn trễ test], [Đơn test])', '0.0%'),
        ('Giảm vượt hẹn (điểm %)', 'IF([Đơn kịch bản] > 0, ([Trễ hiện trạng test] - [Vượt hẹn tính lại]) * 100)', '0.0" điểm %"'),
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


MEASURES['Orders'] += [
    ('Chênh lệch cam kết', '[Thực tế TB] - [Cam kết TB]', '0.00" ngày"'),
    ('Cảnh báo sai', '[Cảnh báo] - [Cảnh báo đúng]', '#,0'),
    ('Tỷ trọng cảnh báo', 'DIVIDE([Cảnh báo], [Đơn test])', '0.0%'),
    ('Phương thức ưu tiên', 'VAR t = FILTER(ADDCOLUMNS(VALUES(Orders[shipping_mode]), "n", [Số đơn], "r", [Tỷ lệ trễ]), [n] > 0) RETURN IF(COUNTROWS(t) > 0, MAXX(TOPN(1, t, [r], DESC, Orders[shipping_mode], ASC), Orders[shipping_mode]), "Không có dữ liệu")', None),
    ('Kỳ phân tích', 'IF([Số đơn] > 0, FORMAT(MIN(Orders[order_date]), "MM/yyyy") & " đến " & FORMAT(MAX(Orders[order_date]), "MM/yyyy"), "Không có dữ liệu")', None),
]
MEASURES['PromiseScenarios'] += [
    ('Nhóm cần rà soát cam kết', 'VAR t = FILTER(ADDCOLUMNS(VALUES(Orders[shipping_mode]), "n", [Đơn kịch bản], "r", [Vượt hẹn tính lại]), [n] > 0) RETURN IF(COUNTROWS(t) > 0, MAXX(TOPN(1, t, [r], DESC, Orders[shipping_mode], ASC), Orders[shipping_mode]), "Không có dữ liệu")', None),
    ('Vượt hẹn nhóm cao nhất', 'MAXX(VALUES(Orders[shipping_mode]), [Vượt hẹn tính lại])', '0.0%'),
]
_ROUTE_FILTER = '''VAR i = SELECTEDVALUE(RouteCases[instance])
VAR s = SELECTEDVALUE(RouteCases[scenario])
VAR k = SELECTEDVALUE(RouteCases[max_vehicles])
VAR q = SELECTEDVALUE(RouteCases[capacity])
VAR m = SELECTEDVALUE(RouteMethods[method])
RETURN IF(HASONEVALUE(RouteCases[case_id]), CALCULATE({aggregate}, REMOVEFILTERS(RouteCases),
RouteCases[instance] = i, RouteCases[scenario] = s, RouteCases[max_vehicles] = k,
RouteCases[capacity] = q, RouteCases[method] = m, RouteCases[status] = "feasible"))'''
MEASURES['RouteCases'] += [
    ('Bản đồ tuyến', 'SELECTEDVALUE(RouteCases[route_image])', None),
    ('Quãng đường đối chiếu', _ROUTE_FILTER.format(aggregate='MAX(RouteCases[distance_units])'), '0.0'),
    ('Xe đối chiếu', _ROUTE_FILTER.format(aggregate='MAX(RouteCases[vehicles_used])'), '#,0'),
    ('Trạng thái đối chiếu', 'IF(ISBLANK([Quãng đường đối chiếu]), "Chưa có lời giải", "Khả thi")', None),
    ('Giảm quãng đường', '''VAR d = [Quãng đường benchmark]
VAR i = SELECTEDVALUE(RouteCases[instance])
VAR s = SELECTEDVALUE(RouteCases[scenario])
VAR k = SELECTEDVALUE(RouteCases[max_vehicles])
VAR q = SELECTEDVALUE(RouteCases[capacity])
VAR b = CALCULATE(MAX(RouteCases[distance_units]), REMOVEFILTERS(RouteCases), RouteCases[instance] = i,
RouteCases[scenario] = s, RouteCases[max_vehicles] = k, RouteCases[capacity] = q,
RouteCases[method] = "nearest_feasible", RouteCases[status] = "feasible")
RETURN IF(NOT ISBLANK(d) && NOT ISBLANK(b), DIVIDE(b - d, b))''', '0.0%'),
]
MEASURES['ModelMetrics'] += [
    ('AP ngoài mẫu', 'CALCULATE(MAX(ModelMetrics[average_precision]), ModelMetrics[partition] = "test")', '0.000'),
    ('AUC ngoài mẫu', 'CALCULATE(MAX(ModelMetrics[roc_auc]), ModelMetrics[partition] = "test")', '0.000'),
    ('Log loss ngoài mẫu', 'CALCULATE(MAX(ModelMetrics[log_loss]), ModelMetrics[partition] = "test")', '0.000'),
]


# Keep numeric measures reusable; card-only measures handle Vietnamese formatting and missing data.
for _table, _items in MEASURES.items():
    for _name, _expression, _format in list(_items):
        if _format:
            _escaped = _format.replace('"', '""')
            _items.append(('Thẻ ' + _name,
                f'IF(ISBLANK([{_name}]), "Chưa có", FORMAT([{_name}], "{_escaped}", "vi-VN"))', None))


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
                    **({'formatString':'yyyy-MM-dd'} if key == 'order_date' else {}),
                    **({'formatString':'MMM yy'} if key == 'month_start' else {}),
                    **({'dataCategory':'ImageUrl','isHidden':True} if key == 'route_image' else {})} for key,value in columns.items()],
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
    tables.append(import_table('PolicySelector', *TABLES['Policies']))
    for name,values in {'RiskThreshold':('GENERATESERIES(CURRENCY(0), CURRENCY(1), CURRENCY(0.01))','decimal'),
                        'KmPerUnit':('GENERATESERIES(0.5, 1.5, 0.1)','double'),
                        'FuelConsumption':('GENERATESERIES(8, 14, 1)','double'),
                        'FuelPrice':('GENERATESERIES(18000, 26000, 1000)','int64')}.items():
        tables.append({'name':name,'columns':[{'name':'Value','dataType':values[1], 'type':'calculatedTableColumn', 'sourceColumn':'[Value]','summarizeBy':'none'}],
            'partitions':[{'name':name,'mode':'import','source':{'type':'calculated','expression':values[0]}}]})
    tables.append({'name':'RouteMethods', 'columns':[
        {'name':'method','dataType':'string','type':'calculatedTableColumn','sourceColumn':'[method]','summarizeBy':'none'},
        {'name':'method_label','dataType':'string','type':'calculatedTableColumn','sourceColumn':'[method_label]','summarizeBy':'none'}],
        'partitions':[{'name':'RouteMethods','mode':'import','source':{'type':'calculated',
            'expression':'DATATABLE("method", STRING, "method_label", STRING, {{"nearest_feasible", "Điểm gần nhất"}, {"ortools", "OR Tools"}})'}}]})
    for table in tables:
        if table['name'] in MEASURES:
            table['measures'] = [{'name':name,'expression':expression, **({'formatString':fmt} if fmt else {}), **({'dataCategory':'ImageUrl'} if name == 'Bản đồ tuyến' else {}), **({'isHidden':True,'displayFolder':'Trình bày'} if name.startswith('Thẻ ') else {})} for name,expression,fmt in MEASURES[table['name']]]
    relationships = []
    for many,column,one,key in [('PromiseScenarios','order_id','Orders','order_id'),('PromiseScenarios','policy_id','Policies','policy_id'),('RouteStops','case_id','RouteCases','case_id')]:
        relationships.append({'name':f'{many}_{column}_{one}','fromTable':many,'fromColumn':column,'toTable':one,'toColumn':key,
                              'fromCardinality':'many','toCardinality':'one','crossFilteringBehavior':'oneDirection'})
    write(MODEL/'definition.pbism',{'$schema':SCHEMA+'item/semanticModel/definitionProperties/1.0.0/schema.json','version':'1.0','settings':{}})
    write(MODEL/'model.bim',{'name':'Delivery','compatibilityLevel':1567,'model':{'culture':'vi-VN','defaultPowerBIDataSourceVersion':'powerBI_V3',
        'sourceQueryCulture':'en-US','expressions':[{'name':'RepoRoot','kind':'m','expression':json.dumps(ROOT.as_posix())+' meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'}],
        'tables':tables,'relationships':relationships,'annotations':[{'name':'PBI_QueryOrder','value':json.dumps(list(TABLES)+['RepoRoot'])}]}})
