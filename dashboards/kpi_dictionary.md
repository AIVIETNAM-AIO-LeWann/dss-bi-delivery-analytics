# Từ điển chỉ số Dashboard

Định nghĩa được đồng bộ từ MEASURES trong scripts/build_powerbi.py.
Mã đơn là Text; tỷ lệ lưu 0–1; ngưỡng dùng số thập phân cố định (CURRENCY).

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

Định dạng: `0.00%`.

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

Định dạng: `0.00%`.

```dax
DIVIDE([Cảnh báo đúng], [Cảnh báo])
```

### Recall theo ngưỡng

Định dạng: `0.00%`.

```dax
DIVIDE([Cảnh báo đúng], [Đơn trễ test])
```

### Bỏ sót

Định dạng: `#,0`.

```dax
[Đơn trễ test] - [Cảnh báo đúng]
```

### P_Late TB test

Định dạng: `0.00%`.

```dax
CALCULATE(AVERAGE(Orders[P_Late]), Orders[partition] = "test")
```

## PromiseScenarios

### Chính sách đang xem

Định dạng: `text`.

```dax
SELECTEDVALUE(Policies[policy_label], "+1 ngày, giữ Same Day")
```

### Đơn kịch bản

Định dạng: `#,0`.

```dax
VAR p = SELECTEDVALUE(Policies[policy_id], "bounded_plus1_keep_same_day") RETURN CALCULATE(COUNTROWS(PromiseScenarios), KEEPFILTERS(Policies[policy_id] = p))
```

### Vượt hẹn tính lại

Định dạng: `0.00%`.

```dax
VAR p = SELECTEDVALUE(Policies[policy_id], "bounded_plus1_keep_same_day") RETURN DIVIDE(CALCULATE(SUM(PromiseScenarios[exceed_proposed]), KEEPFILTERS(Policies[policy_id] = p)), [Đơn kịch bản])
```

### Cam kết mới TB

Định dạng: `0.00" ngày"`.

```dax
VAR p = SELECTEDVALUE(Policies[policy_id], "bounded_plus1_keep_same_day") RETURN CALCULATE(AVERAGE(PromiseScenarios[proposed_days]), KEEPFILTERS(Policies[policy_id] = p))
```

### Tăng cam kết TB

Định dạng: `0.00" ngày"`.

```dax
VAR p = SELECTEDVALUE(Policies[policy_id], "bounded_plus1_keep_same_day") RETURN CALCULATE(AVERAGE(PromiseScenarios[added_days]), KEEPFILTERS(Policies[policy_id] = p))
```

### Trễ hiện trạng test

Định dạng: `0.00%`.

```dax
DIVIDE([Đơn trễ test], [Đơn test])
```

### Giảm vượt hẹn (điểm %)

Định dạng: `0.00" điểm %"`.

```dax
IF([Đơn kịch bản] > 0, ([Trễ hiện trạng test] - [Vượt hẹn tính lại]) * 100)
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

Định dạng: `text`.

```dax
IF(HASONEVALUE(RouteCases[case_id]), IF(SELECTEDVALUE(RouteCases[status]) = "feasible", "Có tuyến khả thi — chưa chứng minh tối ưu", "Chưa tìm được lời giải — không quy về 0"), "Chọn đúng một case_id để xem tuyến và chi phí")
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

## Phạm vi

Orders có một dòng/đơn; PromiseScenarios có một dòng/(đơn test, chính sách). Không đếm lẫn mẫu số.
Rủi ro và chính sách chỉ đánh giá test. ModelMetrics không đổi theo bộ lọc Orders.
Không có mẫu số thì tỷ lệ để trống. Không có lời giải thì distance/cost để trống.
Đơn vị km/nhiên liệu là giả định, ghi trên tiêu đề thay vì nối hậu tố quá dài vào số.
