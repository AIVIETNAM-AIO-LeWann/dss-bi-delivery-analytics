param(
    [Parameter(Mandatory=$true)][int]$Port,
    [Parameter(Mandatory=$true)][string]$ClientDirectory
)
$ErrorActionPreference='Stop'
$repoRoot=Split-Path -Parent $PSScriptRoot
Get-ChildItem -LiteralPath $ClientDirectory -Filter '*.dll' | ForEach-Object {Add-Type -Path $_.FullName}
$connection=[Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$Port")
$connection.Open()
$checks=[System.Collections.Generic.List[object]]::new()
function Query-One([string]$query){
    $command=$connection.CreateCommand()
    $command.CommandText=$query
    $reader=$command.ExecuteReader()
    try{
        if(-not $reader.Read()){throw 'DAX returned no row'}
        $values=@{}
        for($i=0;$i -lt $reader.FieldCount;$i++){
            $name=$reader.GetName($i).Trim('[',']')
            $values[$name]=if($reader.IsDBNull($i)){$null}else{$reader.GetValue($i)}
        }
        return $values
    }finally{$reader.Close()}
}
function Check-Number($actual,$expected,[string]$description){
    if($null -eq $actual -or [Math]::Abs([double]$actual-[double]$expected) -gt 0.0000001){
        throw "$description expected $expected; got $actual"
    }
    $checks.Add(@{description=$description;actual=$actual;expected=$expected})
}
try{
    $overview=Query-One 'EVALUATE ROW("orders", [Số đơn], "late", [Số đơn trễ], "test", [Đơn test], "alerts", [Cảnh báo], "tp", [Cảnh báo đúng], "fn", [Bỏ sót], "precision", [Precision theo ngưỡng], "recall", [Recall theo ngưỡng])'
    Check-Number $overview.orders 62897 'Native analysis denominator'
    Check-Number $overview.late 36048 'Native source late count'
    Check-Number $overview.test 13071 'Native test denominator'
    Check-Number $overview.alerts 4560 'Native alerts at default threshold'
    Check-Number $overview.tp 4057 'Native true positives'
    Check-Number $overview.fn 3467 'Native false negatives'
    Check-Number $overview.precision (4057/4560) 'Native precision'
    Check-Number $overview.recall (4057/7524) 'Native recall'
    $low=Query-One 'EVALUATE CALCULATETABLE(ROW("alerts", [Cảnh báo]), TREATAS({0.4}, RiskThreshold[Value]))'
    Check-Number $low.alerts 13071 'Native threshold 0.4 includes all test orders'
    $standard=Query-One 'EVALUATE CALCULATETABLE(ROW("alerts", [Cảnh báo], "precision", [Precision theo ngưỡng]), TREATAS({"Standard Class"}, Orders[shipping_mode]))'
    Check-Number $standard.alerts 0 'Native zero alerts for Standard Class at threshold 0.5'
    if($null -ne $standard.precision){throw 'Undefined precision must be blank'}
    $checks.Add(@{description='Native undefined precision stays blank';actual=$null})
    $policy=Query-One 'EVALUATE ROW("rate", [Vượt hẹn tính lại], "added", [Tăng cam kết TB], "n", [Đơn kịch bản])'
    Check-Number $policy.rate 0.26815086833448093 'Native default promise exceedance rate'
    Check-Number $policy.added (3.8716242062581285-2.9275495371432942) 'Native promise increase in days'
    Check-Number $policy.n 13071 'Native scenario denominator does not count all five policies'
    $current=Query-One 'EVALUATE CALCULATETABLE(ROW("rate", [Vượt hẹn tính lại], "added", [Tăng cam kết TB]), TREATAS({"current"}, Policies[policy_id]))'
    Check-Number $current.rate (7524/13071) 'Native current policy preserves test late rate'
    Check-Number $current.added 0 'Native current policy adds zero days'
    $route=Query-One 'EVALUATE CALCULATETABLE(ROW("distance", [Quãng đường benchmark], "vehicles", [Số xe sử dụng], "cost", [Nhiên liệu mô phỏng]), TREATAS({"c101|base|ortools"}, RouteCases[case_id]))'
    Check-Number $route.distance 828.936866942834 'Native selected route distance'
    Check-Number $route.vehicles 10 'Native selected route vehicles'
    Check-Number $route.cost (828.936866942834*10/100*22000) 'Native fuel cost with default assumptions'
    $fuel=Query-One 'EVALUATE CALCULATETABLE(ROW("cost", [Nhiên liệu mô phỏng]), TREATAS({"c101|base|ortools"}, RouteCases[case_id]), TREATAS({26000}, FuelPrice[Value]))'
    Check-Number $fuel.cost (828.936866942834*10/100*26000) 'Native fuel price parameter changes cost'
    $missing=Query-One 'EVALUATE CALCULATETABLE(ROW("distance", [Quãng đường benchmark], "cost", [Nhiên liệu mô phỏng]), TREATAS({"c101|fleet10|nearest_feasible"}, RouteCases[case_id]))'
    if($null -ne $missing.distance -or $null -ne $missing.cost){throw 'Unsolved native route must have blank distance/cost'}
    $checks.Add(@{description='Native no-solution distance and cost remain blank';actual=$null})
    $result=@{all_passed=$true;checks_passed=$checks.Count;checks=$checks;scope='DAX executed against the local Power BI Desktop model after native refresh'}
    $output=Join-Path $repoRoot 'reports/dashboard/native_dax_validation.json'
    $result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $output -Encoding utf8
    Write-Output ("PASS: "+$checks.Count+" native DAX checks")
}finally{$connection.Close()}
