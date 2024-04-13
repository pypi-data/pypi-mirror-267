import nni
import numpy as np


params = {
    "features": 512,
    "lr": 0.001,
    "momentum": 0,
}


optimized_params = nni.get_next_parameter()
params.update(optimized_params)


nni.report_final_result({
    "default": np.random.randint(10),
    "experiment_id": nni.get_experiment_id(),
    "trial_id": nni.get_trial_id(),
    "params": params,
})
