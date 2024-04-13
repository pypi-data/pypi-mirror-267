# %%
import skyplan
print(dir(skyplan))
print(skyplan.__version__)

# %%
from skyplan import skyplan
model = skyplan(verbose=10)
model.messages()

# %%
