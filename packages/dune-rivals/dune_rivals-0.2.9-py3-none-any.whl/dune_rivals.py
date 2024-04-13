import ray
import time
import numpy as np

# TODO: double check that obj. store read is < 0.1 (S3 read time)
# DEFINITIONS
SLEEP_SECONDS_PER_TRAVEL_COORD = 0.001
SLEEP_SECONDS_READ_FROM_S3     = 0.100
SLEEP_SECONDS_NOT_ON_SPICE     = 1.000

MAP_DIM = int(1e3)
SPICE_FIELD_PROB = 0.01
SPICE_FILE_SKEW = 0.7
S3_FILE = 2
OBJ_FILE = 1
NUM_ACTORS = 4


class BaseRivalActor:
    """
    DO NOT MODIFY

    Base class with common functionality shared across all Fedaykin and Rival Actors.
    """
    def __init__(self, payload: str):
        self.payload = payload
        self.i = np.random.randint(0, MAP_DIM - 1)
        self.j = np.random.randint(0, MAP_DIM - 1)
        self.gamestate = ray.get_actor("GameState")
        self.spice_loc_map = None
        self.spice_file_map = None
        self.order_map = None
        self.name = None

    def _destroy_spice_field(self) -> bool:
        """
        DO NOT MODIFY

        (Contributes to) destroy(ing) the spice field at location: (self.i, self.j)

        Recall that order_map[(i, j)] returns the order in which your Fedaykin must
        call _destroy_spice_field() in order for the field to be fully destroyed.
        (There is no partial credit for partial destruction).

        The function will return False if the actor fails to destroy the spice field
        because either:

          A. (self.i, self.j) is not a valid spice field location, or
          B. at least one Fedaykin preceding this one in the order_map has not yet
             called _destroy_spice_field() at this location

        The function returns True if the call to destroy the spice field is successful.
        """
        # if this isn't a spice field, incur a delay and return False
        if not self.spice_loc_map[(self.i, self.j)]:
            print(f"{self.name} tried to destroy spice at {(self.i, self.j)}, but this is not a Spice location.")  # TODO: fix for h2h
            print(f"{self.name} sleeping for {SLEEP_SECONDS_NOT_ON_SPICE} seconds")
            time.sleep(SLEEP_SECONDS_NOT_ON_SPICE)
            return False

        # if file is "on S3" simulate extra delay for the network request
        if self.spice_file_map[(self.i, self.j)] == S3_FILE:
            print(f"{self.name} fetching spice field object from S3 for {(self.i, self.j)}")
            time.sleep(SLEEP_SECONDS_READ_FROM_S3)
        else:
            print(f"{self.name} fetching spice field object from OBJECT STORE for {(self.i, self.j)}")

        # get spice field object
        spice_field_refs = ray.get(self.gamestate.get_spice_field_refs.remote("southern"))  # TODO: fix for h2h
        spice_field = ray.get(spice_field_refs[(self.i, self.j)])

        # check if spice field object can be written to
        write_order = self.order_map[(self.i, self.j)]
        try:
            write_idx = np.where(write_order == self.id)[0][0]
        except:
            print(f"{self.name} tried to destroy spice at {(self.i, self.j)} but is not a valid destroyer ({list(write_order)})")

        if np.array_equal(spice_field["writes"], write_order[:write_idx]):
            spice_field["writes"].append(self.id)
            if np.array_equal(spice_field["writes"], write_order):
                spice_field["payload"] = self.payload
                print(f"{self.name} DESTROYED SPICE FIELD AT ({(self.i, self.j)})")
            else:
                print(f"{self.name} partially destroyed spice field at ({(self.i, self.j)})")
            self.gamestate.update_spice_field_ref.remote(spice_field, self.i, self.j, "southern")  # TODO: fix for h2h
            return True

        else:
            print(f"{self.name} tried to destroy spice at {(self.i, self.j)} but current vs. destruction is: ({spice_field['writes']}) vs. ({list(write_order)})")
            return False


    def _ride_sandworm(self, new_i: int, new_j: int) -> None:
        """
        DO NOT MODIFY

        Moves your Fedaykin to the coordinates (new_i, new_j) and sleeps for the
        appropriate travel duration.
        """
        assert 0 <= new_i and new_i < MAP_DIM, f"New coord. i: {new_i} is off the map"
        assert 0 <= new_j and new_j < MAP_DIM, f"New coord. i: {new_j} is off the map"

        # calculate manhattan distance of movement
        delta_i = abs(new_i - self.i)
        delta_j = abs(new_j - self.j)
        total_dist = delta_i + delta_j

        # sleep for travel duration
        time.sleep(total_dist * SLEEP_SECONDS_PER_TRAVEL_COORD)

        # update coordinates
        self.i = new_i
        self.j = new_j


@ray.remote(num_cpus=0.1, resources={"worker3": 1e-4})
class Noop12(BaseRivalActor):
    def __init__(self, payload: str):
        super().__init__(payload)
        self.id = 12
        self.name = "Noop12"

    def start(self, spice_loc_map: np.ndarray, spice_file_map: np.ndarray, order_map: dict):
        pass

@ray.remote(num_cpus=0.1, resources={"worker4": 1e-4})
class Noop34(BaseRivalActor):
    def __init__(self, payload: str):
        super().__init__(payload)
        self.id = 34
        self.name = "Noop34"

    def start(self, spice_loc_map: np.ndarray, spice_file_map: np.ndarray, order_map: dict):
        pass


##############################################################################################
################################         Silly Goose          ################################
##############################################################################################
class BaseSillyGoose(BaseRivalActor):
    def __init__(self, payload: str):
        super().__init__(payload)

    def start(self, spice_loc_map: np.ndarray, spice_file_map: np.ndarray, order_map: dict):
        # set these state variables
        self.spice_loc_map = spice_loc_map
        self.spice_file_map = spice_file_map
        self.order_map = order_map

    def start(self, spice_loc_map: np.ndarray, spice_file_map: np.ndarray, order_map: dict):
        # set these state variables
        self.spice_loc_map = spice_loc_map
        self.spice_file_map = spice_file_map
        self.order_map = order_map

    def get_spice_loc_map(self):
        return self.spice_loc_map


@ray.remote(num_cpus=0.8, name="SillyGoose1", resources={"worker3": 1e-4})
class SillyGoose1(BaseSillyGoose):
    """
    SillyGoose1 is the leader. It picks which spice field to target and moves all
    other Geese to that target. Once the necessary Geese arrive, it instructs the
    Geese to destroy spice in the specified order.
    """
    def __init__(self, payload: str):
        super().__init__(payload)
        self.id = 1
        self.name = "SillyGoose1"

    def start(self, spice_loc_map: np.ndarray, spice_file_map: np.ndarray, order_map: dict):
        # set these state variables
        self.spice_loc_map = spice_loc_map
        self.spice_file_map = spice_file_map
        self.order_map = order_map

        # confirm that other actors have set variables
        all_ready = False
        while not all_ready:
            all_ready = True
            for id in [2, 3, 4]:
                goose = ray.get_actor(f"SillyGoose{id}")
                loc_map = ray.get(goose.get_spice_loc_map.remote())
                all_ready = all_ready and (loc_map is not None)

        # get spice locations and iterate over them to destroy spice
        out = np.where(spice_loc_map==1)
        for i, j in zip(out[0], out[1]):
            # move Geese that are needed to location (i,j)
            geese_ids = self.order_map[(i,j)]
            for goose_id in geese_ids:
                if goose_id != 1:
                    goose = ray.get_actor(f"SillyGoose{goose_id}")
                    goose._ride_sandworm.remote(i, j)
                else:
                    self._ride_sandworm(i, j)

            # destroy spice in synchronous fashion
            for goose_id in geese_ids:
                if goose_id != 1:
                    goose = ray.get_actor(f"SillyGoose{goose_id}")
                    ray.get(goose._destroy_spice_field.remote())
                else:
                    self._destroy_spice_field()


@ray.remote(num_cpus=0.8, name="SillyGoose2", resources={"worker3": 1e-4})
class SillyGoose2(BaseSillyGoose):
    def __init__(self, payload: str):
        super().__init__(payload)
        self.id = 2
        self.name = "SillyGoose2"
    
    # def start(self, spice_loc_map: np.ndarray, spice_file_map: np.ndarray, order_map: dict):
    #     print(f"SillyGoose{self.id} starting")
    #     # set these state variables
    #     self.spice_loc_map = spice_loc_map
    #     self.spice_file_map = spice_file_map
    #     self.order_map = order_map
    #     print(f"SillyGoose{self.id} self.spice_loc_map is None?: {self.spice_loc_map is None}")

    # def get_spice_loc_map(self):
    #     return self.spice_loc_map

@ray.remote(num_cpus=0.8, name="SillyGoose3", resources={"worker4": 1e-4})
class SillyGoose3(BaseSillyGoose):
    def __init__(self, payload: str):
        super().__init__(payload)
        self.id = 3
        self.name = "SillyGoose3"
    
    # def start(self, spice_loc_map: np.ndarray, spice_file_map: np.ndarray, order_map: dict):
    #     print(f"SillyGoose{self.id} starting")
    #     # set these state variables
    #     self.spice_loc_map = spice_loc_map
    #     self.spice_file_map = spice_file_map
    #     self.order_map = order_map
    #     print(f"SillyGoose{self.id} self.spice_loc_map is None?: {self.spice_loc_map is None}")

    # def get_spice_loc_map(self):
    #     return self.spice_loc_map

@ray.remote(num_cpus=0.8, name="SillyGoose4", resources={"worker4": 1e-4})
class SillyGoose4(BaseSillyGoose):
    def __init__(self, payload: str):
        super().__init__(payload)
        self.id = 4
        self.name = "SillyGoose4"

    # def start(self, spice_loc_map: np.ndarray, spice_file_map: np.ndarray, order_map: dict):
    #     print(f"SillyGoose{self.id} starting")
    #     # set these state variables
    #     self.spice_loc_map = spice_loc_map
    #     self.spice_file_map = spice_file_map
    #     self.order_map = order_map
    #     print(f"SillyGoose{self.id} self.spice_loc_map is None?: {self.spice_loc_map is None}")

    # def get_spice_loc_map(self):
    #     return self.spice_loc_map

##############################################################################################
###############################         Glossu Rabban          ###############################
##############################################################################################


##############################################################################################
################################         Feyd Rautha          ################################
##############################################################################################