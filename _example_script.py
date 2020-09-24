"""INITIALIZE WITH PISA DATA AND VARIABLES OF INTEREST."""


# %% NO PARAMETERS
#  selections enter manually
#  original data reloaded
# OUTPUT = initialize(None, None)

from pisa_explorer import initialize
OUTPUT = initialize()


# %% SELECTIONS ENTER MANUALLY
#  avoid reloading original data by passing global copy to initialize
#  user prompt

from pisa_explorer import get_original, initialize
if 'PISA2012_ORIGINAL' not in globals():
    PISA2012_ORIGINAL = get_original()
OUTPUT = initialize(None, PISA2012_ORIGINAL)


# %% SELECTIONS FROM OBJECT
#  avoid reloading original data by passing global copy to initialize
#  previous output

from pisa_explorer import get_original, initialize
if 'PISA2012_ORIGINAL' not in globals():
    PISA2012_ORIGINAL = get_original()
OUTPUT = initialize(OUTPUT, PISA2012_ORIGINAL)


# %% SELECTION FROM PRESET
#  avoid reloading original data by passing global copy to initialize
#  preset selection from global

from pisa_explorer import get_original, initialize, PRESET1
if 'PISA2012_ORIGINAL' not in globals():
    PISA2012_ORIGINAL = get_original()
OUTPUT = initialize(PRESET1.copy(), PISA2012_ORIGINAL)


# %% SELECTIONS FROM PREVIOUSY SAVED
#  avoid reloading original data by passing global copy to initialize
#  directly load old file

from pisa_explorer import get_original, initialize, load_saved
if 'PISA2012_ORIGINAL' not in globals():
    PISA2012_ORIGINAL = get_original()
OUTPUT = initialize(load_saved(), PISA2012_ORIGINAL)
