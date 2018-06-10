import googlemaps
from datetime import datetime
import json
from gmplot import gmplot
import pandas as pd
import random
import pickle

"""Notes:
Need 2 request:
    1) current -> parking : via driving
    2) parking pace -> destination : via walking

Input: Current location: Address
       Parking location: geocode
       Destination locatin: Address

Output:
      Driving distance nad duration to parking
      Walking distane and duration from parking to place of destination


Bounding rect:


"""

L = (32.713772, -117.161030)
U = (32.717852, -117.160088)
B = (32.709409, -117.157039)
R = (32.711554, -117.150366)


DST = (32.714711, -117.155766)

SEED = 1337
random.seed(SEED)


def sample_drivers(num=50):
    drivers = []
    for n in range(50):
        drivers.append( (random.uniform(B[0], U[0]), random.uniform(L[1],R[1])) )
    return drivers


def main():
    with open('API.json', 'r') as fp:
        key = json.load(fp)

    gmaps = googlemaps.Client(key=key['api_key'])

    df = _prepare_data()
    df = filter_by_rect(df)

    # sampling parkings
    parkings = df.sample(n=10, random_state=SEED)["geo"].tolist()
    drivers = sample_drivers(num=50)
    destination = DST

    dataset = {"output": []}
    for d in drivers:
        out = ask_google(gmaps, d, parkings, destination, verbose=False)
        dataset["output"].append(out)
    pickle.dump(dataset, open( "dataset.p", "wb" ) )

    print(dataset["output"][0])

    #loc = "San Diego High School 1405 Park Blvd San Diego, CA 92101"
    #dest = " The New Children’s Museum 200 W Island Ave San Diego, CA 92101"

    ## Ask database for parking spots, belowe is temporary
    #park = "Wells Fargo Bank 610 1st Ave San Diego, CA 92101"
    #park2 = "Ralphs 101 G St San Diego, CA 92101"


    #print(ask_google(gmaps, loc, [park, park2], dest, verbose=False))


def ask_google(gmaps, current_loc, parking_loc, destination_loc, verbose=False):
    """Uses google maps API

    Parameters
    ----------
    gmaps : obj
                  Logged client object form googlemaps package

    current_loc : str or (float, float)
                  Your initial, starting location

    parking_loc : list of str or list of (float, float)
                  Loacations of considered parkings lots

    destination_loc : str or (float, float)
                  Your final destination
    Returns
    -------
    result : dict(list(dict))
    Dictonary with keys: ["driving", "walking"]
        where:
        result["driving"] = [result_for_parking1, result_for_parkin2, ...]
            where:
            result_for_parkingx is dict with keys: ["distance", "duration"]
                where distance is in meters and duration in seconds
    """


    # Request distances via car transit
    now = datetime.now()
    driving_result = gmaps.distance_matrix(
        origins=current_loc,
        destinations=parking_loc,
        mode="driving",
        units="metric",
        departure_time=now,)

    # Request distances via walking transit
    walking_result = gmaps.distance_matrix(
        origins=parking_loc,
        destinations=destination_loc,
        mode="walking",
        units="metric",
        departure_time=now,)

    # FIXME:
    #if verbose:
        #print("+-----Driving-----+")
        #print("FROM: ", driving_result['origin_addresses'][0])
        #print("TO  : ", driving_result['destination_addresses'][0])
        #print("Distance: ", driving_data["distance"]["text"])
        #print("Duration: ", driving_data["duration"]["text"])
        ##print(driving_result.keys())
        ##print(driving_data.keys())
        #print()
        #print("+-----Walking-----+")
        #print("FROM: ", walking_result['origin_addresses'][0])
        #print("TO  : ", walking_result['destination_addresses'][0])
        #print("Distance: ", walking_data["distance"]["text"])
        #print("Duration: ", walking_data["duration"]["text"])

    # yeah xd
    return {
        "driving": [{"distance":
                     driving_result["rows"][0]["elements"][i]["distance"]["value"],
                     "duration":
                     driving_result["rows"][0]["elements"][i]["duration"]["value"]}
                    for i in range(len(driving_result["rows"][0]["elements"]))],

        "walking": [{"distance":
                     walking_result["rows"][i]["elements"][0]["distance"]["value"],
                     "duration":
                     walking_result["rows"][i]["elements"][0]["duration"]["value"]}
                     for i in range(len(walking_result["rows"]))]
    }



def plot_column(gmap, df, column_name, marker=False, filename=None):
    """Plots single column onto map

    Parameters
    ----------
    column_name : str
                  Name of column in string to plot
    filename : str or None
               Name of file where plot will be saved, if None default filename
               is the name od plotted column with '.html' extension
    """

    print("dupa")
    zones_df = dict(tuple(df.groupby(column_name)))
    zones = [zones_df[x] for x in zones_df]
    for i, zone in enumerate(zones):
        lats, lons = zip(*zone['geo'].values.tolist())
        if marker:
            for d in zone['geo'].values.tolist():
                gmap.marker(d[0], d[1], 'black')
        else:
            gmap.scatter(lats, lons, _rand_color(), size=10, marker=False)

    print("dupa")
    #if filename is None:
        #filename = column_name + ".html"
    #gmap.draw(filename)
    #print("dupa")


def plot_drivers(gmap, drivers):
    lats, lons = zip(*drivers)
    for d in drivers:
        gmap.marker(d[0], d[1], 'cornflowerblue')

def plot_destinations(gmap, destination):
    gmap.marker(destination[0], destination[1], 'red')

def main_plot():
    #plot_column('zone')
    #plot_column('area')

    df = _prepare_data()
    df = filter_by_rect(df)

    # sampling parkings
    df = df.sample(n=10, random_state=SEED)
    drivers = sample_drivers(num=50)

    gmap = gmplot.GoogleMapPlotter.from_geocode("San Diego")
    plot_column(gmap, df, 'price', marker=True)
    plot_drivers(gmap, drivers)
    plot_destinations(gmap, DST)

    gmap.draw("eh.html")


def filter_by_rect(df):
    #df = _prepare_data()
    df = df[df['latitude'].between(B[0], U[0], inclusive=False)]
    df = df[df['longitude'].between(L[1], R[1], inclusive=False)]
    return df


def _prepare_data(verbose=False):
    """Prepare dataset for ploting and further computation

    Returns
    -------
    df : DataFrame
         Pandas Dataframe with columns:
         ['geo', 'latitude', 'longitude', 'zone', 'area', 'time_max', 'price',
          'hour_open', 'hour_close', 'day_open', 'day_close']
         NOTE: 'geo' is just List('latitude', 'longitude')

    """

    df = pd.read_csv("../dataset/parking_data.csv")
    data = df['config_name']
    df['geo'] = df[['latitude', 'longitude']].values.tolist()
    df = df[['geo','latitude','longitude', 'zone', 'area']]

    time_max = data.str.extract('(?P<time_max>\w+\s\w+\s\w+)\s')
    price = data.str.extract('\s(?P<price>\$\d+.\d+)\s')
    hour_open = data.str.extract('\s(?P<hour_open>\d+[a-z]{2})-')
    hour_close = data.str.extract('-(?P<hour_close>\d+[a-z]{2})\s')
    day_open = data.str.extract('\s(?P<day_open>[A-Z][a-z]+)-')
    day_close = data.str.extract('-(?P<day_close>[A-Z][a-z]+)')
    df = pd.concat([df, time_max, price, hour_open, hour_close, day_open,
                     day_close], axis=1)


    if verbose:
        print("\n+--Unique values for each column--+")
        print("+---------------------------------+")
        print("price: ", df["price"].unique())
        print("time_max: ", df["time_max"].unique())
        print("hour_open: ", df["hour_open"].unique())
        print("hour_close: ", df["hour_close"].unique())
        print("day_open: ", df["day_open"].unique())
        print("day_close: ", df["day_close"].unique())
        print("+---------------------------------+\n")

    return df


def _rand_color(string=True):
    SIX_DIGIT_HEX_INT_MIN = 1048576
    SIX_DIGIT_HEX_INT_MAX = 16777215

    c = hex(random.randrange(SIX_DIGIT_HEX_INT_MIN, SIX_DIGIT_HEX_INT_MAX))
    if string:
        return "#" + str(c)[2:]
    else:
        return c


if __name__ == "__main__":
    #main()
    #main_plot()
    #create_map()
    #main_plot()
