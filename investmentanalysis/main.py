from investmentanalysis.ml_workflow.concrete_flows import (
    ClosePredictionWorkflow,
    VolumePredictionWorkflow,
)


if __name__ == "__main__":
    predict_close = ClosePredictionWorkflow()
    predict_volume = VolumePredictionWorkflow()

    predict_close.run_workflow()
    predict_volume.run_workflow()
