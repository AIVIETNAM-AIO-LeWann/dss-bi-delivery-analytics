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


# ---- Control-panel redesign: dynamic text, whole-period figures and SVG pictures ----
from .powerbi_svg import (funnel_expression, keypad_expression, logo_expression, ring_expression,
                          thermometer_expression, track_expression, RED, TEAL)

MEASURES['Orders'] += [
    ('Số đơn toàn kỳ', 'CALCULATE([Số đơn], REMOVEFILTERS(Orders))', '#,0'),
    ('Số tháng toàn kỳ', 'CALCULATE(DISTINCTCOUNT(Orders[month_start]), REMOVEFILTERS(Orders))', '#,0'),
    ('Số thị trường toàn kỳ', 'CALCULATE(DISTINCTCOUNT(Orders[market]), REMOVEFILTERS(Orders))', '#,0'),
    ('Tỷ lệ trễ toàn kỳ', 'CALCULATE([Tỷ lệ trễ], REMOVEFILTERS(Orders))', '0.0%'),
    ('Chiếm đơn trễ', 'DIVIDE([Số đơn trễ], CALCULATE([Số đơn trễ], REMOVEFILTERS(Orders[shipping_mode])))', '0.0%'),
    ('Chữ cam kết thực tế', 'IF([Số đơn] > 0, FORMAT([Cam kết TB], "0.00", "vi-VN") & " → " & FORMAT([Thực tế TB], "0.00", "vi-VN") & " ngày", "Chưa có")', None),
    ('Chữ đơn và đơn trễ', 'IF([Số đơn] > 0, FORMAT([Số đơn], "#,0", "vi-VN") & " / " & FORMAT([Số đơn trễ], "#,0", "vi-VN"), "Chưa có")', None),
    ('Chữ đơn trễ', 'FORMAT([Số đơn trễ], "#,0", "vi-VN") & " đơn trễ"', None),
    ('Chữ đơn đúng hạn', 'FORMAT([Số đơn] - [Số đơn trễ], "#,0", "vi-VN") & " đúng hạn"', None),
    ('Nhãn so với trung bình', 'IF([Số đơn] = 0, "", IF([Tỷ lệ trễ] > [Tỷ lệ trễ toàn kỳ], "▲ TRÊN TRUNG BÌNH", "▼ DƯỚI TRUNG BÌNH"))', None),
    ('Cảnh báo đúng trên đơn test', 'DIVIDE([Cảnh báo đúng], [Đơn test])', '0.0%'),
    ('Cảnh báo sai trên đơn test', 'DIVIDE([Cảnh báo sai], [Đơn test])', '0.0%'),
    ('Bỏ sót trên đơn test', 'DIVIDE([Bỏ sót], [Đơn test])', '0.0%'),
    ('Đơn trễ trên đơn test', 'DIVIDE([Đơn trễ test], [Đơn test])', '0.0%'),
    ('Kết luận tổng quan', """VAR t = FILTER(ADDCOLUMNS(VALUES(Orders[shipping_mode]), "n", [Số đơn], "r", [Tỷ lệ trễ], "l", [Số đơn trễ]), [n] > 0)
VAR a = TOPN(1, t, [r], DESC, Orders[shipping_mode], ASC)
VAR b = TOPN(1, t, [l], DESC, Orders[shipping_mode], ASC)
VAR total = SUMX(t, [l])
RETURN IF(COUNTROWS(t) = 0, "Không có dữ liệu",
    MAXX(a, Orders[shipping_mode]) & " có tỷ lệ trễ cao nhất (" & FORMAT(MAXX(a, [r]), "0.0%", "vi-VN") & "); "
    & MAXX(b, Orders[shipping_mode]) & " có nhiều đơn trễ nhất (" & FORMAT(DIVIDE(MAXX(b, [l]), total), "0.0%", "vi-VN") & " số đơn trễ).")""", None),
    ('Kết luận rủi ro', 'IF([Cảnh báo] = 0, "Không có cảnh báo ở ngưỡng đang chọn.", "Cảnh báo đúng " & FORMAT([Precision theo ngưỡng], "0.0%", "vi-VN") & " nhưng chỉ bắt được " & FORMAT([Recall theo ngưỡng], "0.0%", "vi-VN") & " đơn trễ; " & FORMAT([Bỏ sót], "#,0", "vi-VN") & " đơn trễ chưa được cảnh báo.")', None),
    ('Đơn mỗi tháng', 'DIVIDE([Số đơn], DISTINCTCOUNT(Orders[month_start]))', '#,0'),
    ('Chữ cảnh báo đúng', 'FORMAT([Cảnh báo đúng], "#,0", "vi-VN") & " đúng"', None),
    ('Chữ cảnh báo', 'FORMAT([Cảnh báo], "#,0", "vi-VN") & " được báo"', None),
    ('Chữ bắt được', 'FORMAT([Cảnh báo đúng], "#,0", "vi-VN") & " bắt được"', None),
    ('Chữ đơn trễ test', 'FORMAT([Đơn trễ test], "#,0", "vi-VN") & " đơn trễ"', None),
    ('Chữ cảnh báo sai', '"Có thêm " & FORMAT([Cảnh báo sai], "#,0", "vi-VN") & " cảnh báo sai (báo trễ nhưng giao đúng hạn)"', None),
    ('Logo', logo_expression(), None),
    ('Vòng tỷ lệ trễ', ring_expression('[Tỷ lệ trễ]', RED, 'đơn giao trễ hạn'), None),
    ('Vòng độ chính xác', ring_expression('[Precision theo ngưỡng]', TEAL, 'đúng trong số cảnh báo'), None),
    ('Vòng độ bao phủ', ring_expression('[Recall theo ngưỡng]', RED, 'bắt được trong đơn trễ'), None),
    ('Thanh tỷ lệ trễ', track_expression('[Tỷ lệ trễ]', '[Tỷ lệ trễ toàn kỳ]'), None),
    ('Nhiệt kế toàn kỳ', thermometer_expression('[Tỷ lệ trễ toàn kỳ]'), None),
    ('Bàn phím nhiệt', keypad_expression('[Tỷ lệ trễ]', 'Orders[shipping_mode]', 'Orders[market]'), None),
    ('Phễu phát hiện', funnel_expression('[Đơn test]', '[Đơn trễ test]', '[Cảnh báo đúng]', '[Bỏ sót]'), None),
]
_POLICY = 'COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day")'
MEASURES['PromiseScenarios'] += [
    ('Cam kết hiện tại TB', 'CALCULATE(AVERAGE(PromiseScenarios[proposed_days]), KEEPFILTERS(Policies[policy_id] = "current"))', '0.00" ngày"'),
    ('Đơn vượt hẹn tính lại', 'ROUND([Vượt hẹn tính lại] * [Đơn kịch bản], 0)', '#,0'),
    ('Đơn hết vượt hẹn', '[Đơn trễ test] - [Đơn vượt hẹn tính lại]', '#,0'),
    ('Dự phòng', f'VAR p = {_POLICY} RETURN DIVIDE(CALCULATE(SUM(PromiseScenarios[fallback]), KEEPFILTERS(Policies[policy_id] = p)), [Đơn kịch bản])', '0.0%'),
    ('Kết luận cam kết', 'IF([Đơn kịch bản] = 0, "Không có dữ liệu", [Chính sách đang xem] & " đưa tỷ lệ vượt hẹn từ " & FORMAT([Trễ hiện trạng test], "0.0%", "vi-VN") & " xuống " & FORMAT([Vượt hẹn tính lại], "0.0%", "vi-VN") & ", đổi lại khách chờ thêm trung bình " & FORMAT([Tăng cam kết TB], "0.00", "vi-VN") & " ngày; đây là đổi cam kết, thời gian giao thực tế không đổi.")', None),
    ('Chữ hiện tại', '"hiện tại " & FORMAT([Trễ hiện trạng test], "0.0%", "vi-VN")', None),
    ('Chữ đơn vượt hẹn', 'FORMAT([Đơn vượt hẹn tính lại], "#,0", "vi-VN") & " đơn vượt hẹn"', None),
    ('Vòng vượt hẹn', ring_expression('[Vượt hẹn tính lại]', RED, 'đơn vượt hẹn tính lại'), None),
]
MEASURES['RouteCases'] += [
    ('Chữ tiêu hao', 'FORMAT(SELECTEDVALUE(FuelConsumption[Value], 10), "0", "vi-VN") & " lít / 100 km"', None),
    ('Chữ giá nhiên liệu', 'FORMAT(SELECTEDVALUE(FuelPrice[Value], 22000), "#,0", "vi-VN") & " VND / lít"', None),
    ('Chữ quy đổi', 'FORMAT(SELECTEDVALUE(KmPerUnit[Value], 1), "0.0", "vi-VN") & " km / đơn vị"', None),
    ('Chữ tải trọng', 'IF(HASONEVALUE(RouteCases[case_id]), FORMAT(SELECTEDVALUE(RouteCases[capacity]), "#,0", "vi-VN") & " / xe", "—")', None),
    ('Chữ xe tối đa', 'IF(HASONEVALUE(RouteCases[case_id]), FORMAT(SELECTEDVALUE(RouteCases[max_vehicles]), "0", "vi-VN") & " xe", "—")', None),
    ('Kết luận tuyến', 'IF(NOT ISBLANK([Quãng đường benchmark]), "Phương án này dùng " & FORMAT([Số xe sử dụng], "0", "vi-VN") & " xe và " & FORMAT([Quãng đường benchmark], "#,0.0", "vi-VN") & " đơn vị quãng đường" & IF(NOT ISBLANK([Giảm quãng đường]), ", ngắn hơn " & FORMAT([Giảm quãng đường], "0.0%", "vi-VN") & " so với điểm gần nhất cùng cấu hình", "") & "; nhiên liệu mô phỏng " & FORMAT([Nhiên liệu mô phỏng], "#,0", "vi-VN") & " VND theo giả định đã chọn.", [Trạng thái tuyến])', None),
]
IMAGE_MEASURES = {'Bản đồ tuyến', 'Logo', 'Vòng tỷ lệ trễ', 'Vòng độ chính xác', 'Vòng độ bao phủ', 'Vòng vượt hẹn',
                  'Thanh tỷ lệ trễ', 'Nhiệt kế toàn kỳ', 'Bàn phím nhiệt', 'Phễu phát hiện'}



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
            table['measures'] = [{'name':name,'expression':expression, **({'formatString':fmt} if fmt else {}), **({'dataCategory':'ImageUrl'} if name in IMAGE_MEASURES else {}), **({'isHidden':True,'displayFolder':'Trình bày'} if name.startswith('Thẻ ') else {}), **({'isHidden':True,'displayFolder':'Hình ảnh'} if name in IMAGE_MEASURES and name != 'Bản đồ tuyến' else {})} for name,expression,fmt in MEASURES[table['name']]]
    relationships = []
    for many,column,one,key in [('PromiseScenarios','order_id','Orders','order_id'),('PromiseScenarios','policy_id','Policies','policy_id'),('RouteStops','case_id','RouteCases','case_id')]:
        relationships.append({'name':f'{many}_{column}_{one}','fromTable':many,'fromColumn':column,'toTable':one,'toColumn':key,
                              'fromCardinality':'many','toCardinality':'one','crossFilteringBehavior':'oneDirection'})
    write(MODEL/'definition.pbism',{'$schema':SCHEMA+'item/semanticModel/definitionProperties/1.0.0/schema.json','version':'1.0','settings':{}})
    write(MODEL/'model.bim',{'name':'Delivery','compatibilityLevel':1567,'model':{'culture':'vi-VN','defaultPowerBIDataSourceVersion':'powerBI_V3',
        'sourceQueryCulture':'en-US','expressions':[{'name':'RepoRoot','kind':'m','expression':json.dumps(ROOT.as_posix())+' meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'}],
        'tables':tables,'relationships':relationships,'annotations':[{'name':'PBI_QueryOrder','value':json.dumps(list(TABLES)+['RepoRoot'])}]}})
