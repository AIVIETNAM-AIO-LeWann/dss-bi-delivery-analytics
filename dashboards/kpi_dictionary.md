# Định nghĩa chỉ số Power BI

Measures số giữ kiểu dữ liệu để lọc và tính tiếp. Measures `Thẻ …` được ẩn, chỉ định dạng tiếng Việt cho thẻ KPI; giá trị không xác định hiển thị “Chưa có”.

## Orders

### Số đơn

Định dạng: `#,0`.

```dax
COALESCE(COUNTROWS(Orders), 0)
```

### Số đơn trễ

Định dạng: `#,0`.

```dax
COALESCE(SUM(Orders[late_delivery_risk]), 0)
```

### Tỷ lệ trễ

Định dạng: `0.0%`.

```dax
DIVIDE([Số đơn trễ], [Số đơn])
```

### Cam kết TB

Định dạng: `0.00" ngày"`.

```dax
AVERAGE(Orders[shipping_days_scheduled])
```

### Thực tế TB

Định dạng: `0.00" ngày"`.

```dax
AVERAGE(Orders[shipping_days_actual])
```

### Đơn test

Định dạng: `#,0`.

```dax
CALCULATE([Số đơn], Orders[partition] = "test")
```

### Ngưỡng cảnh báo

Định dạng: `0.00`.

```dax
SELECTEDVALUE(RiskThreshold[Value], 0.5)
```

### Cảnh báo

Định dạng: `#,0`.

```dax
VAR t = [Ngưỡng cảnh báo] RETURN CALCULATE([Đơn test], KEEPFILTERS(Orders[P_Late] >= t), KEEPFILTERS(NOT ISBLANK(Orders[P_Late])))
```

### Cảnh báo đúng

Định dạng: `#,0`.

```dax
CALCULATE([Cảnh báo], Orders[late_delivery_risk] = 1)
```

### Đơn trễ test

Định dạng: `#,0`.

```dax
CALCULATE([Số đơn trễ], Orders[partition] = "test")
```

### Precision theo ngưỡng

Định dạng: `0.0%`.

```dax
DIVIDE([Cảnh báo đúng], [Cảnh báo])
```

### Recall theo ngưỡng

Định dạng: `0.0%`.

```dax
DIVIDE([Cảnh báo đúng], [Đơn trễ test])
```

### Bỏ sót

Định dạng: `#,0`.

```dax
[Đơn trễ test] - [Cảnh báo đúng]
```

### P_Late TB test

Định dạng: `0.0%`.

```dax
CALCULATE(AVERAGE(Orders[P_Late]), Orders[partition] = "test")
```

### Chênh lệch cam kết

Định dạng: `0.00" ngày"`.

```dax
[Thực tế TB] - [Cam kết TB]
```

### Cảnh báo sai

Định dạng: `#,0`.

```dax
[Cảnh báo] - [Cảnh báo đúng]
```

### Tỷ trọng cảnh báo

Định dạng: `0.0%`.

```dax
DIVIDE([Cảnh báo], [Đơn test])
```

### Phương thức ưu tiên

Định dạng: văn bản.

```dax
VAR t = FILTER(ADDCOLUMNS(VALUES(Orders[shipping_mode]), "n", [Số đơn], "r", [Tỷ lệ trễ]), [n] > 0) RETURN IF(COUNTROWS(t) > 0, MAXX(TOPN(1, t, [r], DESC, Orders[shipping_mode], ASC), Orders[shipping_mode]), "Không có dữ liệu")
```

### Kỳ phân tích

Định dạng: văn bản.

```dax
IF([Số đơn] > 0, FORMAT(MIN(Orders[order_date]), "MM/yyyy") & " đến " & FORMAT(MAX(Orders[order_date]), "MM/yyyy"), "Không có dữ liệu")
```

## PromiseScenarios

### Chính sách đang xem

Định dạng: văn bản.

```dax
COALESCE(SELECTEDVALUE(PolicySelector[policy_label]), "Thêm một ngày")
```

### Đơn kịch bản

Định dạng: `#,0`.

```dax
VAR p = COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day") RETURN CALCULATE(COUNTROWS(PromiseScenarios), KEEPFILTERS(Policies[policy_id] = p))
```

### Vượt hẹn tính lại

Định dạng: `0.0%`.

```dax
VAR p = COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day") RETURN DIVIDE(CALCULATE(SUM(PromiseScenarios[exceed_proposed]), KEEPFILTERS(Policies[policy_id] = p)), [Đơn kịch bản])
```

### Cam kết mới TB

Định dạng: `0.00" ngày"`.

```dax
VAR p = COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day") RETURN CALCULATE(AVERAGE(PromiseScenarios[proposed_days]), KEEPFILTERS(Policies[policy_id] = p))
```

### Tăng cam kết TB

Định dạng: `0.00" ngày"`.

```dax
VAR p = COALESCE(SELECTEDVALUE(Policies[policy_id]), SELECTEDVALUE(PolicySelector[policy_id]), "bounded_plus1_keep_same_day") RETURN CALCULATE(AVERAGE(PromiseScenarios[added_days]), KEEPFILTERS(Policies[policy_id] = p))
```

### Trễ hiện trạng test

Định dạng: `0.0%`.

```dax
DIVIDE([Đơn trễ test], [Đơn test])
```

### Giảm vượt hẹn (điểm %)

Định dạng: `0.0" điểm %"`.

```dax
IF([Đơn kịch bản] > 0, ([Trễ hiện trạng test] - [Vượt hẹn tính lại]) * 100)
```

### Nhóm cần rà soát cam kết

Định dạng: văn bản.

```dax
VAR t = FILTER(ADDCOLUMNS(VALUES(Orders[shipping_mode]), "n", [Đơn kịch bản], "r", [Vượt hẹn tính lại]), [n] > 0) RETURN IF(COUNTROWS(t) > 0, MAXX(TOPN(1, t, [r], DESC, Orders[shipping_mode], ASC), Orders[shipping_mode]), "Không có dữ liệu")
```

### Vượt hẹn nhóm cao nhất

Định dạng: `0.0%`.

```dax
MAXX(VALUES(Orders[shipping_mode]), [Vượt hẹn tính lại])
```

## RouteCases

### Quãng đường benchmark

Định dạng: `0.00`.

```dax
IF(HASONEVALUE(RouteCases[case_id]) && SELECTEDVALUE(RouteCases[status]) = "feasible", SELECTEDVALUE(RouteCases[distance_units]))
```

### Số xe sử dụng

Định dạng: `#,0`.

```dax
IF(HASONEVALUE(RouteCases[case_id]) && SELECTEDVALUE(RouteCases[status]) = "feasible", SELECTEDVALUE(RouteCases[vehicles_used]))
```

### Km mô phỏng

Định dạng: `0.00`.

```dax
[Quãng đường benchmark] * SELECTEDVALUE(KmPerUnit[Value], 1)
```

### Nhiên liệu mô phỏng

Định dạng: `#,0`.

```dax
[Km mô phỏng] * SELECTEDVALUE(FuelConsumption[Value], 10) / 100 * SELECTEDVALUE(FuelPrice[Value], 22000)
```

### Trạng thái tuyến

Định dạng: văn bản.

```dax
IF(HASONEVALUE(RouteCases[case_id]), IF(SELECTEDVALUE(RouteCases[status]) = "feasible", "Có tuyến khả thi — chưa chứng minh tối ưu", "Chưa tìm được lời giải — không quy về 0"), "Chọn đúng một case_id để xem tuyến và chi phí")
```

### Bản đồ tuyến

Định dạng: văn bản.

```dax
SELECTEDVALUE(RouteCases[route_image])
```

### Quãng đường đối chiếu

Định dạng: `0.0`.

```dax
VAR i = SELECTEDVALUE(RouteCases[instance])
VAR s = SELECTEDVALUE(RouteCases[scenario])
VAR k = SELECTEDVALUE(RouteCases[max_vehicles])
VAR q = SELECTEDVALUE(RouteCases[capacity])
VAR m = SELECTEDVALUE(RouteMethods[method])
RETURN IF(HASONEVALUE(RouteCases[case_id]), CALCULATE(MAX(RouteCases[distance_units]), REMOVEFILTERS(RouteCases),
RouteCases[instance] = i, RouteCases[scenario] = s, RouteCases[max_vehicles] = k,
RouteCases[capacity] = q, RouteCases[method] = m, RouteCases[status] = "feasible"))
```

### Xe đối chiếu

Định dạng: `#,0`.

```dax
VAR i = SELECTEDVALUE(RouteCases[instance])
VAR s = SELECTEDVALUE(RouteCases[scenario])
VAR k = SELECTEDVALUE(RouteCases[max_vehicles])
VAR q = SELECTEDVALUE(RouteCases[capacity])
VAR m = SELECTEDVALUE(RouteMethods[method])
RETURN IF(HASONEVALUE(RouteCases[case_id]), CALCULATE(MAX(RouteCases[vehicles_used]), REMOVEFILTERS(RouteCases),
RouteCases[instance] = i, RouteCases[scenario] = s, RouteCases[max_vehicles] = k,
RouteCases[capacity] = q, RouteCases[method] = m, RouteCases[status] = "feasible"))
```

### Trạng thái đối chiếu

Định dạng: văn bản.

```dax
IF(ISBLANK([Quãng đường đối chiếu]), "Chưa có lời giải", "Khả thi")
```

### Giảm quãng đường

Định dạng: `0.0%`.

```dax
VAR d = [Quãng đường benchmark]
VAR i = SELECTEDVALUE(RouteCases[instance])
VAR s = SELECTEDVALUE(RouteCases[scenario])
VAR k = SELECTEDVALUE(RouteCases[max_vehicles])
VAR q = SELECTEDVALUE(RouteCases[capacity])
VAR b = CALCULATE(MAX(RouteCases[distance_units]), REMOVEFILTERS(RouteCases), RouteCases[instance] = i,
RouteCases[scenario] = s, RouteCases[max_vehicles] = k, RouteCases[capacity] = q,
RouteCases[method] = "nearest_feasible", RouteCases[status] = "feasible")
RETURN IF(NOT ISBLANK(d) && NOT ISBLANK(b), DIVIDE(b - d, b))
```

## RouteStops

### Node tuyến

Định dạng: `#,0`.

```dax
SELECTEDVALUE(RouteStops[node])
```

### Thứ tự dừng

Định dạng: `#,0`.

```dax
SELECTEDVALUE(RouteStops[sequence])
```

### Tọa độ X

Định dạng: `0.0`.

```dax
IF(HASONEVALUE(RouteCases[case_id]), AVERAGE(RouteStops[x]))
```

### Tọa độ Y

Định dạng: `0.0`.

```dax
IF(HASONEVALUE(RouteCases[case_id]), AVERAGE(RouteStops[y]))
```

## ModelMetrics

### AUC baseline test

Định dạng: `0.000`.

```dax
CALCULATE(MAX(ModelMetrics[roc_auc]), ModelMetrics[model] = "mode_baseline", ModelMetrics[partition] = "test")
```

### Log loss baseline test

Định dạng: `0.000`.

```dax
CALCULATE(MAX(ModelMetrics[log_loss]), ModelMetrics[model] = "mode_baseline", ModelMetrics[partition] = "test")
```

### AP ngoài mẫu

Định dạng: `0.000`.

```dax
CALCULATE(MAX(ModelMetrics[average_precision]), ModelMetrics[partition] = "test")
```

### AUC ngoài mẫu

Định dạng: `0.000`.

```dax
CALCULATE(MAX(ModelMetrics[roc_auc]), ModelMetrics[partition] = "test")
```

### Log loss ngoài mẫu

Định dạng: `0.000`.

```dax
CALCULATE(MAX(ModelMetrics[log_loss]), ModelMetrics[partition] = "test")
```

## Phạm vi

Orders có một dòng/đơn. PromiseScenarios có một dòng/(đơn test, chính sách). Rủi ro và cam kết chỉ tính trên test. PolicySelector điều khiển phương án đang xem; từng dòng Policies vẫn tính chính sách riêng. ModelMetrics không đổi theo bộ lọc Orders. Solomon độc lập với DataCo. Không có mẫu số, lời giải hoặc đối chứng khả thi thì chỉ tiêu tương ứng để trống.
