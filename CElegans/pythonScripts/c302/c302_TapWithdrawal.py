import c302
import sys

import neuroml.writers as writers

    
def setup(parameter_set, 
          generate=False,
          duration=1000,
          dt=0.05,
          target_directory='examples'):
    
    exec('from parameters_%s import ParameterisedModel'%parameter_set)
    params = ParameterisedModel()

    params.set_bioparameter("unphysiological_offset_current", "0pA", "Testing TapWithdrawal", "0")
    params.set_bioparameter("unphysiological_offset_current_del", "0 ms", "Testing TapWithdrawal", "0")
    params.set_bioparameter("unphysiological_offset_current_dur", "2000 ms", "Testing TapWithdrawal", "0")

    cells = ['AVAL', 'AVAR', 'AVBL', 'AVBR', 'PVCL', 'PVCR', 'AVDL', 'AVDR', 'DVA', 'PVDL', 'PVDR', 'PLML', 'PLMR', 'AVM', 'ALML', 'ALMR']
    cells_to_stimulate = []
    #cells_to_stimulate = ['PLML', 'PLMR']
    #cells_to_stimulate = ['AVM']

    cells_to_plot = ['AVAL', 'AVAR', 'AVBL', 'AVBR', 'PLML', 'PLMR', 'AVM']

    reference = "c302_%s_TapWithdrawal"%parameter_set
    
    
    if generate:
        nml_doc = c302.generate(reference, 
                 params, 
                 cells=cells,
                 cells_to_plot=cells_to_plot,
                 cells_to_stimulate=cells_to_stimulate, 
                 duration=2000,
                 dt=0.1, 
                 validate=(parameter_set!='B'),
                 target_directory = target_directory)
                 
        stim_amplitude = "5pA"

        c302.add_new_input(nml_doc, "PLML", "100ms", "400ms", stim_amplitude, params)
        c302.add_new_input(nml_doc, "PLMR", "100ms", "400ms", stim_amplitude, params)
        c302.add_new_input(nml_doc, "AVM", "1000ms", "400ms", stim_amplitude, params)
        
        nml_file = target_directory+'/'+reference+'.nml'
        writers.NeuroMLWriter.write(nml_doc, nml_file) # Write over network file written above...

        print("(Re)written network file to: "+nml_file)
             
    return cells, cells_to_stimulate, params, False
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)