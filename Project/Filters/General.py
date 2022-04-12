
def pre_process(config):
    config["desired_controller_eigenvalues"] = tuple(
        config["desired_controller_eigenvalues"]
    )
    return config
    
