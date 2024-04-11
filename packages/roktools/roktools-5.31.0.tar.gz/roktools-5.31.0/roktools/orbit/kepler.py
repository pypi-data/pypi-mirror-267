from dataclasses import dataclass
import datetime
import math

@dataclass
class Kepler(object):
    """
    Data class to represent a satellite orbit in an inertial reference frame
    """

    """ Time of Ephemeris """
    toe: datetime.datetime

    """ Argument of the perigee [rad] """
    arg_perigee_rad:float

    """ Eccentricity """
    eccentricity:float

    """ Inclination [rad] """
    inclination_rad:float

    """ Mean anomaly [rad] """
    mean_anomaly_rad:float

    """ Mean motion [rad/s] """
    mean_motion_rad_per_s:float

    """ Right ascension of the ascending node [rad] """
    raan_rad:float

    """  First derivative of the mean anomaly [rad/s] """
    n_dot_rad_per_s:float


    def __repr__(self) -> str:
        out = f"""
        toe: {self.toe}
        n_dot[rad/s]: {self.n_dot_rad_per_s}
        inclination[deg]: {math.degrees(self.inclination_rad)}
        RAAN[deg]: {math.degrees(self.raan_rad)}
        eccentricity: {self.eccentricity}
        arg_perigee[deg]: {math.degrees(self.arg_perigee_rad)}
        mean anomaly[deg]: {math.degrees(self.mean_anomaly_rad)}
        mean motion[rad/s]: {self.mean_motion_rad_per_s}
        """
        return out