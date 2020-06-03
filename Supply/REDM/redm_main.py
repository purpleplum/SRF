import pandas
from utils.interface import \
    load_parameters, empty_folder, save_to_file, get_args
from utils.analysis import analyze_mgra
from modeling.developer import develop
from modeling.filter import filter_mgras
import utils.config as config
from tqdm import tqdm


def step(mgras, progress):
    """
    develop enough land to meet demand for this year.
    """
    progress.set_description('filtering')
    filtered = filter_mgras(mgras)
    progress.update()
    return develop(mgras, filtered, progress)


def run(mgra_dataframe):
    output_dir = config.parameters['output_directory']
    simulation_years = config.parameters['simulation_years']
    simulation_begin = config.parameters['simulation_begin']
    debug = config.parameters['debug']

    if debug:
        print('input frame description')
        analyze_mgra(mgra_dataframe, output_dir)
    # the number of tqdm progress bar steps per simulation year
    checkpoints = 8
    progress = tqdm(desc='progress', total=simulation_years *
                    checkpoints, position=0)
    for i in range(simulation_years):
        forecast_year = simulation_begin + i + 1
        progress.set_description('starting year {}'.format(i+1))
        if debug:
            print('simulating year {} ({})'.format(i + 1, forecast_year))

        mgra_dataframe, progress = step(mgra_dataframe, progress)
        progress.update()
        if debug:
            print('updated frame:')
            analyze_mgra(mgra_dataframe, output_dir)

        progress.set_description('saving year {}'.format(i+1))
        save_to_file(mgra_dataframe, output_dir, 'year{}_{}.csv'.format(
            i + 1, forecast_year))
        progress.update()
    progress.close()
    return


if __name__ == "__main__":
    # load parameters
    config.parameters = load_parameters('test_parameters.yaml')

    # re-enable normal parameters once full dataset is available
    # args = get_args()
    # if args.test:
    #     config.parameters = load_parameters('test_parameters.yaml')
    # else:
    #     config.parameters = load_parameters('parameters.yaml')

    if config.parameters is not None:
        output_dir = config.parameters['output_directory']
        empty_folder(output_dir)
        save_to_file(config.parameters, output_dir, 'parameters.txt')

        mgra_dataframe = pandas.read_csv(config.parameters['input_filename'])

        run(mgra_dataframe)

    else:
        print('could not load parameters, exiting')