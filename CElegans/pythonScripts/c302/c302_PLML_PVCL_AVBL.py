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

    params.set_bioparameter("unphysiological_offset_current", "4.5pA", "Testing TapWithdrawal", "0")
    params.set_bioparameter("unphysiological_offset_current_del", "100 ms", "Testing TapWithdrawal", "0")
    params.set_bioparameter("unphysiological_offset_current_dur", "800 ms", "Testing TapWithdrawal", "0")

    cells = ['PLML', 'PVCL', 'AVBL']
    cells_to_stimulate = ['PLML']
    cells_to_plot = cells

    reference = "c302_%s_PLM_PVC_AVB"%parameter_set
    
    if generate:
        nml_doc = c302.generate(reference, 
                 params, 
                 cells=cells,
                 cells_to_plot=cells_to_plot,
                 cells_to_stimulate=cells_to_stimulate,
                 override_conn_polarity={
                     'PVCL-AVBL': 'exc',
                 },
                 conn_number_override={
                 },
                 include_muscles=False,
                 duration=duration,
                 dt=dt,
                 validate=(parameter_set!='B'),
                 target_directory = target_directory)

        #stim_amplitude = "4.5pA"
        #stim_amplitude = "5.135697186048022pA"

        #c302.add_new_input(nml_doc, "PLML", "50ms", "800ms", stim_amplitude, params)
        
        #nml_file = target_directory+'/'+reference+'.nml'
        #writers.NeuroMLWriter.write(nml_doc, nml_file) # Write over network file written above...

        #print("(Re)written network file to: "+nml_file)
             
    return cells, cells_to_stimulate, params, False
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'C2'
    
    setup(parameter_set, generate=True)