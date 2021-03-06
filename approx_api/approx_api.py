from datetime import datetime, timedelta

import psycopg2
import simplejson as json


class ApproximationAPI:
    def __init__(self, host, dbname, user, pw, port):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.port = port
        self.pw = pw
        self.con = None

    ###############
    # CONNECTIONS #
    ###############
    def connect(self):
        self.con = psycopg2.connect(
            "host='" + self.host + "' dbname='" + self.dbname + "' user='" + self.user + "' password='" + self.pw + "' port='" + self.port + "'")
        return self.con

    def close_connect(self):
        self.con.close()
        self.con = None

    # test connection
    def test(self):
        print("Testing connection to database: " + self.dbname)
        print("Host: " + self.host)
        print("User: " + self.user)

        self.con = self.connect()
        print("Successfully connected to database")

        if self.con:
            self.close_connect()
            print("Successfully closed connection from database")


            #################
            # FUNCTIONALITY #
            #################

    def get_location_name(self, lat, lon):
        try:
            statement = ''' 
                SELECT tweet_collector_barangays.name_3, city_municipalities.name_2, provinces.name_1
                FROM city_municipalities 
                INNER JOIN tweet_collector_barangays ON city_municipalities.id_2 = tweet_collector_barangays.id_2
                INNER JOIN provinces ON provinces.id_1 = city_municipalities.id_1
                WHERE ST_INTERSECTS(ST_PointFromText('POINT( ''' + str(lon) + " " + str(lat) + ''')', 4326), tweet_collector_barangays.geom);
            '''
            cur = self.con.cursor()
            cur.execute(statement)
            fetch = cur.fetchone()
            cur.close()
            if (fetch != None):
                out = {"name": {"barangay": fetch[0], "city": fetch[1], "province": fetch[2]},
                       "geo": {"lat": str(lat), "lon": str(lon)}}
            else:
                out = {"name": "N/A", "geo": {"lat": lat, "lon": lon}}
        except:
            out = {"name": "N/A", "geo": {"lat": lat, "lon": lon}}
        return out

    # all tweets
    def get_tweets(self, collection_id):
        statement = ''' 
            SELECT tweet_id, created_at, tweet_user, tweet_text, tweet_lat, tweet_lon, tweet_user_location, radius, tweet_json
            FROM tweet_collector_tweets
            WHERE collection_id = ''' + str(collection_id) + '''
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"created_at": str(arr[i][1]), "user": arr[i][2],
                              "profile_pic": json.loads(arr[i][8])['user']['profile_image_url'], "text": arr[i][3],
                              "user_location": arr[i][6], "location": {"lat": str(arr[i][4]), "lon": str(arr[i][5])},
                              "radius": arr[i][7]}
        cur.close()
        return dic

    def get_geo_tweets(self, collection_id):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon, created_at
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id)
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]), "lon": str(arr[i][3]),
                              "created_at": str(arr[i][4])}
        cur.close()
        return dic

    def get_geo_tweets_ph(self, collection_id):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon, created_at
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
            AND is_inPH(cast(tweet_lon as varchar), cast(tweet_lat as varchar)); 
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]), "lon": str(arr[i][3]),
                              "created_at": str(arr[i][4])}
        cur.close()
        return dic

    def get_geo_tweets_hour(self, collection_id, date_start, date_end):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon, created_at
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
            AND created_at BETWEEN ''' + date_start.strftime("'%Y-%m-%d %H:%M:%S'") + ''' AND ''' + date_end.strftime(
            "'%Y-%m-%d %H:%M:%S'")
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]), "lon": str(arr[i][3]),
                              "created_at": str(arr[i][4])}
        cur.close()
        return dic

    def get_geo_tweets_hour_ph(self, collection_id, date_start, date_end):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon, created_at
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
            AND created_at BETWEEN ''' + date_start.strftime("'%Y-%m-%d %H:%M:%S'") + ''' AND ''' + date_end.strftime(
            "'%Y-%m-%d %H:%M:%S'") + '''
            AND is_inPH(cast(tweet_lon as varchar), cast(tweet_lat as varchar)); 
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]), "lon": str(arr[i][3]),
                              "created_at": str(arr[i][4])}
        cur.close()
        return dic

    def get_all_geo_tweets(self):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon, created_at
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]), "lon": str(arr[i][3]),
                              "created_at": str(arr[i][4])}
        cur.close()
        return dic

    def get_all_geo_tweets_ph(self):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon, created_at
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL
            AND is_inPH(cast(tweet_lon as varchar), cast(tweet_lat as varchar)); 
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]), "lon": str(arr[i][3]),
                              "created_at": str(arr[i][4])}
        cur.close()
        return dic

    # for tweets to be geolocated using model
    def get_non_geo_tweets(self, collection_id, limit, last_tweet_id):

        if last_tweet_id:
            statement = ''' 
                SELECT tweet_id, tweet_text, created_at
                FROM tweet_collector_tweets
                WHERE tweet_lat ISNULL AND tweet_lon ISNULL  AND tweet_id > ''' + str(
                last_tweet_id) + '''AND collection_id = ''' + str(collection_id) + '''
                ORDER BY tweet_id ASC LIMIT + ''' + str(limit) + '''
            '''
        else:
            statement = ''' 
                SELECT tweet_id, tweet_text, created_at
                FROM tweet_collector_tweets
                WHERE tweet_lat ISNULL AND tweet_lon ISNULL AND collection_id = ''' + str(collection_id) + '''
		ORDER BY tweet_id ASC LIMIT + ''' + str(limit) + '''
            '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "created_at": str(arr[i][2])}
        cur.close()
        return dic

    def get_all_non_geo_tweets(self):
        statement = ''' 
            SELECT tweet_id, tweet_text, created_at
            FROM tweet_collector_tweets
            WHERE tweet_lat ISNULL AND tweet_lon ISNULL
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "created_at": str(arr[i][2])}
        cur.close()
        return dic

    def get_non_geo_tweets_hour(self, collection_id, date_start, date_end):
        statement = ''' 
            SELECT tweet_id, tweet_text, created_at
            FROM tweet_collector_tweets
            WHERE tweet_lat ISNULL AND tweet_lon ISNULL AND collection_id = ''' + str(collection_id) + '''
            AND created_at BETWEEN ''' + date_start.strftime("'%Y-%m-%d %H:%M:%S'") + ''' AND ''' + date_end.strftime(
            "'%Y-%m-%d %H:%M:%S'")
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "created_at": str(arr[i][2])}
        cur.close()
        return dic

    # for visualization of tweets
    def get_tweet_vis_data(self, collection_id):
        statement = ''' 
            SELECT tweet_id, created_at, tweet_user, tweet_text, tweet_lat, tweet_lon, tweet_user_location, radius, tweet_json, is_approximated
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            location = self.get_location_name(arr[i][4], arr[i][5])
            dic[arr[i][0]] = {"created_at": str(arr[i][1]), "user": json.loads(arr[i][8])['user']['name'],  "username": arr[i][2], "profile_pic": json.loads(arr[i][8])['user']['profile_image_url'], "text": arr[i][3], "user_location": arr[i][6], "location": location, "radius": arr[i][7], "is_approximated": arr[i][9]}
        cur.close()
        return dic

    def get_tweet_vis_data_ph(self, collection_id):
        statement = ''' 
            SELECT tweet_id, created_at, tweet_user, tweet_text, tweet_lat, tweet_lon, tweet_user_location, radius, tweet_json, is_approximated
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
            AND is_inPH(cast(tweet_lon as varchar), cast(tweet_lat as varchar)); 
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            location = self.get_location_name(arr[i][4], arr[i][5])
            dic[arr[i][0]] = {"created_at": str(arr[i][1]), "user": json.loads(arr[i][8])['user']['name'],  "username": arr[i][2], "profile_pic": jaon.loads(arr[i][8])['user']['profile_image_url'], "text": arr[i][3], "user_location": arr[i][6], "location": location, "radius": arr[i][7], "is_approximated": arr[i][9]}

        cur.close()
        return dic

        # for limited

    def get_tweet_vis_data_limit(self, collection_id, start_row):
        statement = ''' 
            SELECT tweet_id, created_at, tweet_user, tweet_text, tweet_lat, tweet_lon, tweet_user_location, radius, tweet_json, is_approximated
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
            ORDER BY created_at
            LIMIT 10 OFFSET ''' + str(start_row)

        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            location = self.get_location_name(arr[i][4], arr[i][5])
            dic[arr[i][0]] = {"created_at": str(arr[i][1]), "user": json.loads(arr[i][8])['user']['name'], "username": arr[i][2], "profile_pic": json.loads(arr[i][8])['user']['profile_image_url'], "text": arr[i][3], "user_location": arr[i][6], "location": location, "radius": arr[i][7],"is_approximated": arr[i][9]}

        cur.close()
        return dic

    def get_tweet_vis_data_limit_ph(self, collection_id, start_row):
        statement = ''' 
            SELECT tweet_id, created_at, tweet_user, tweet_text, tweet_lat, tweet_lon, tweet_user_location, radius, tweet_json, is_approximated
            FROM tweet_collector_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND collection_id = ''' + str(collection_id) + '''
            AND is_inPH(cast(tweet_lon as varchar), cast(tweet_lat as varchar))
            ORDER BY created_at
            LIMIT 10 OFFSET ''' + str(start_row)

        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            location = self.get_location_name(arr[i][4], arr[i][5])
            dic[arr[i][0]] = {"created_at": str(arr[i][1]), "user": arr[i][8]['user']['name'],  "username": arr[i][2], "profile_pic": arr[i][8]['user']['profile_image_url'], "text": arr[i][3], "user_location": arr[i][6], "location": location, "radius": arr[i][7], "is_approximated": arr[i][9]}

        cur.close()
        return dic

    def update_location(self, tweet_id, lat, lon, radius):
        statement = ''' 
            UPDATE tweet_collector_tweets
            SET tweet_lat = ''' + str(lat) + ''', tweet_lon = ''' + str(lon) + ''', radius = ''' + str(radius) + ''', is_approximated = false
            WHERE tweet_id =''' + str(tweet_id) + ''';
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        self.con.commit()
        cur.close()
        return "Success!"

    def get_tweet_json(self, collection_id):
        statement = ''' 
            SELECT tweet_json
            FROM tweet_collector_tweets
            WHERE collection_id = ''' + str(collection_id) + '''
            LIMIT 1
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        return cur.fetchone()

    def get_collections(self):
        statement = '''SELECT id, title FROM tweet_collector_collections'''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"title": str(arr[i][1])}
        cur.close()
        return dic

    def get_collection_id(self, batch_name):
        statement = "SELECT id FROM tweet_collector_collections where batch_name = '" + str(batch_name) + "'"
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchone()

        dic = {"id": arr[0]}

        return dic

    def get_tweets(self, collection_id, date_start, date_end):
        statement = ''' 
            SELECT tweet_id, created_at, tweet_user, tweet_text, tweet_lat, tweet_lon, tweet_user_location, radius, tweet_json
            FROM tweet_collector_tweets
            WHERE collection_id = ''' + str(collection_id) + '''
            AND created_at BETWEEN ''' + created_at + ''' AND ''' + date_end
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"created_at": str(arr[i][1]), "user": arr[i][2],
                              "profile_pic": json.loads(arr[i][8])['user']['profile_image_url'], "text": arr[i][3],
                              "user_location": arr[i][6], "location": {"lat": str(arr[i][4]), "lon": str(arr[i][5])},
                              "radius": arr[i][7]}
        cur.close()
        return dic

    def update_model(self):
        # Should return tweets from the past 6 hours only
        date_end = datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")
        date_start = (datetime.now() - timedelta(hours=6)).strftime("'%Y-%m-%d %H:%M:%S'")
        statement = ''' 
	     DELETE FROM model_tweets;
             INSERT INTO model_tweets SELECT * FROM tweet_collector_tweets
             WHERE created_at BETWEEN ''' + date_start + ''' AND ''' + date_end

        print(statement)
        cur = self.con.cursor()
        cur.execute(statement)
        print("Performed insert")
        return 0

    def get_model_tweets(self, model_id):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon, created_at
            FROM model_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND model_name  = ''' + "'" + str(model_id) + "'"
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]), "lon": str(arr[i][3]),
                              "created_at": str(arr[i][4])}
        cur.close()
        return dic

    def get_model_tweets_ph(self, model_id):
        statement = ''' 
            SELECT tweet_id, tweet_text, tweet_lat, tweet_lon, created_at
            FROM model_tweets
            WHERE tweet_lat IS NOT NULL AND tweet_lon IS NOT NULL AND model_name = ''' + "'" + str(model_id) + "'" + '''
            AND is_inPH(cast(tweet_lon as varchar), cast(tweet_lat as varchar)); 
        '''
        cur = self.con.cursor()
        cur.execute(statement)
        arr = cur.fetchall()

        dic = {}
        for i in range(len(arr)):
            dic[arr[i][0]] = {"text": str(arr[i][1]), "lat": str(arr[i][2]), "lon": str(arr[i][3]),
                              "created_at": str(arr[i][4])}
        cur.close()
        return dic

    ###########################
    # FOR LOCAL DATABASE TEST #
    ###########################
    def setup(self):
        if self.con:
            cur = self.con.cursor()
            cur.execute(open("migrations/tables.sql", "r").read())
            print("Created tables.")
            cur.execute(open("migrations/phl_adm0s.sql", "r").read())
            print("Imported gis data to countries table")
            cur.execute(open("migrations/phl_adm1s.sql", "r").read())
            print("Imported gis data to provinces table")
            cur.execute(open("migrations/phl_adm2s.sql", "r").read())
            print("Imported gis data to city_municipalities table")
            cur.execute(open("migrations/phl_adm3s.sql", "r").read())
            print("Imported gis data to tweet_collector_barangays table")
            self.con.commit()
            cur.close()
        else:
            self.connect()
            self.setup()

    def import_tweets(self, filename):
        statement = ''' 
            COPY %s FROM STDIN WITH 
                CSV 
                HEADER
                DELIMITER AS ',' 
            '''
        my_file = open(filename)
        cur = self.con.cursor()
        cur.copy_expert(sql=statement % 'tweets', file=my_file)
        self.con.commit()
        cur.close()
        print("Successfully imported tweets")
