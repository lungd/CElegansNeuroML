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
                 override_conn_polarity={
                     'ALML-ALML':'inh',
                     'ALML-AVDR': 'inh',
                     'ALML-PVCL': 'inh',
                     'ALML-PVCR': 'inh',
                     'ALMR-PVCR': 'inh',
                     'AVAL-AVAR': 'inh',
                     'AVAL-AVBL':'inh',
                     'AVAL-AVBR': 'inh',
                     'AVAL-AVDL': 'inh',
                     'AVAL-AVDR': 'inh',
                     'AVAL-PVCL': 'inh',
                     'AVAL-PVCR': 'inh',
                     'AVAR-AVAL': 'inh',
                     'AVAR-AVBL': 'inh',
                     'AVAR-AVBR': 'inh',
                     'AVAR-AVDL': 'inh',
                     'AVAR-AVDR': 'inh',
                     'AVAR-PVCL': 'inh',
                     'AVAR-PVCR': 'inh',
                     'AVBL-AVAL': 'inh',
                     'AVBL-AVAR': 'inh',
                     'AVBL-AVBR': 'inh',
                     'AVBL-AVDL': 'inh',
                     'AVBL-AVDR': 'inh',
                     'AVBL-DVA': 'inh',
                     'AVBL-PVCR': 'inh',
                     'AVBR-AVAL': 'inh',
                     'AVBR-AVAR': 'inh',
                     'AVBR-AVBL': 'inh',
                     'AVBR-AVDL': 'inh',
                     'AVDL-AVAL': 'exc', #
                     'AVDL-AVAR': 'exc', #
                     'AVDL-PVCL': 'exc', #
                     'AVDR-AVAL': 'exc', #
                     'AVDR-AVAR': 'exc', #
                     'AVDR-AVBL': 'exc', #
                     'AVDR-AVDL': 'exc', #
                     'AVM-AVBL':  'inh',
                     'AVM-AVBR':  'inh',
                     'AVM-AVDL':'inh',
                     'AVM-AVDR':'inh',
                     'AVM-PVCL':  'inh',
                     'AVM-PVCR':  'inh',
                     'DVA-AVAL':  'inh',
                     'DVA-AVAR':  'inh',
                     'DVA-AVBL':  'inh',
                     'DVA-AVBR':'inh',
                     'DVA-AVDR':'inh',
                     'DVA-PVCL':  'inh',
                     'DVA-PVCR':  'inh',
                     'PLMR-AVAL': 'inh',
                     'PLMR-AVAR': 'inh',
                     'PLMR-AVDL': 'inh',
                     'PLMR-AVDR': 'inh',
                     'PLMR-DVA':  'inh',
                     'PLMR-PVCL': 'inh',
                     'PVCL-AVAL': 'exc', #
                     'PVCL-AVAR': 'exc', #
                     'PVCL-AVBL': 'exc', #
                     'PVCL-AVBR': 'exc', #
                     'PVCL-AVDL': 'exc', #
                     'PVCL-AVDR': 'exc', #
                     'PVCL-DVA':  'exc', #
                     'PVCL-PVCR': 'exc', #
                     'PVCR-AVAL': 'exc', #
                     'PVCR-AVAR': 'exc', #
                     'PVCR-AVBL': 'exc', #
                     'PVCR-AVBR': 'exc', #
                     'PVCR-AVDL': 'exc', #
                     'PVCR-AVDR': 'exc', #
                     'PVCR-PVCL': 'exc', #
                     'PVCR-PVDL': 'exc', #
                     'PVDL-AVDL':'inh',
                     'PVDL-AVDR':'inh',
                     'PVDL-AVAL': 'inh',
                     'PVDL-AVAR': 'inh',
                     'PVDL-PVDR':'inh',
                     'PVDL-PVCL': 'inh',
                     'PVDL-PVCR': 'inh',
                     'PVDR-AVAL': 'inh',
                     'PVDR-AVAR': 'inh',
                     'PVDR-AVDL':'inh',
                     'PVDR-DVA':  'inh',
                     'PVDR-PVCL': 'inh',
                     'PVDR-PVCR': 'inh',
                     'PVDR-PVDL': 'inh',

                     },
                 conn_number_override={
                     #'AVAL-PVCL':30, # 21
                     #'AVAL-PVCR':28, # 16
                     #'AVAR-PVCL':30, # 20
                     #'AVAR-PVCR':30, # 20

                     #'AVBR-AVDL':20, # 4

                     #'AVM-PVCL':20, # 10
                     #'AVM-PVCR':30, # 17

                     #'AVAL-AVBL':15, # 2
                     #'AVAR-AVBL':15, # 3
                     #'AVAR-AVBR':16, # 4
                     #'AVBL-AVAL':18, # 9
                     #'AVBL-AVAR':28, # 14
                     #'AVBR-AVAL':20, # 10
                     #'AVBR-AVAR':28, # 14                     
 
                 
                 },
                 include_muscles=False,
                 duration=2000,
                 dt=0.05,
                 validate=(parameter_set!='B'),
                 target_directory = target_directory)

        stim_amplitude = "5pA"
        #stim_amplitude = "5.135697186048022pA"

        c302.add_new_input(nml_doc, "PLML", "100ms", "600ms", stim_amplitude, params)
        c302.add_new_input(nml_doc, "PLMR", "100ms", "600ms", stim_amplitude, params)

        c302.add_new_input(nml_doc, "AVM", "1000ms", "400ms", stim_amplitude, params)
        
        nml_file = target_directory+'/'+reference+'.nml'
        writers.NeuroMLWriter.write(nml_doc, nml_file) # Write over network file written above...

        print("(Re)written network file to: "+nml_file)
             
    return cells, cells_to_stimulate, params, False
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'C2'
    
    setup(parameter_set, generate=True)
