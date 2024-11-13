from datacontract.data_contract import DataContract

data_contract = DataContract(data_contract_file="dcdqexample.0.2.1.datacontract.yaml")
run = data_contract.test()
if not run.has_passed():
    print("Data quality validation failed.")
    # Abort pipeline, alert, or take corrective actions...
