#Derrick Chuong
#Facebook Graph API is no longer available of Aug 7,2016
import json
import requests

ACCESS_TOKEN = "EAAWJaOclG7kBAAOfGKZC9PZBfCIfsyAx3j6K1NOBKdTUW1HwTb97oO5S8KZCnQNxGZCZCWu2frEj1X9Jyfv0EGxXUpwUOgJQF2brTZBE2Yaew62UJ9SOXPkZCHVQqRMUzo9G6wsx1p5ayduWO7ZAxbrkok5zwdF1E2cZD"
USER_ID = "me"  

class FbGraph:
  @staticmethod
  # a recursive method to go through the dictionary
  def loopDict(d, album_list):
    for k,v in d.items():
        if isinstance(v, dict):
            FbGraph.loopDict(v,album_list)
        else:
            #facebook has a paging and data as the key
            if k == 'data':
                for line in v: # give {id,count, name}
                    temp = []
                    for key,value in line.items():
                        #print (key, value)
                        temp.append((key,value))
                    album_list.append(temp)
    return album_list

  @staticmethod
  #helper function to check the nested dictionary / list for the album ID we are looking for
  def get_album_photo(d, album_list, compare_id ):
    for k,v in d.items():
        temp = []
        if isinstance(v, dict):
            FbGraph.get_album_photo(v,album_list,compare_id)
        if isinstance(v, list):
            for line in v:
                FbGraph.get_album_photo(line,album_list,compare_id)
        temp.append(d)
        
        if v in compare_id:
            album_list.append((temp , v))
    return album_list
        
  @staticmethod
  #helper function to print out the name of the photos
  def print_name(d):
    for k,v in d.items():
        if isinstance(v, dict):
            FbGraph.print_name(v)
        if isinstance(v, list):
            for line in v:
                FbGraph.print_name(line)
        else:
            if 'name' == k:
                print v
                
  @staticmethod
  def about_me():
    body = {
      'access_token': ACCESS_TOKEN,
      'fields': "id,name,languages,birthday,education"
    }
    url = "https://graph.facebook.com/v2.6/%s/" % USER_ID
    r = requests.get(url, params=body)
    #print r.text
    output = json.loads(r.text)
    # TASK 1: Update the output to include the languages I speak, my birthday, and where I went to school    
    return output

  @staticmethod
  def my_albums():
    # TASK 2: Output my album ids, album names, and the number of photos in each album
    body = {
        'access_token': ACCESS_TOKEN,
        'fields' : "albums{id,name,count}"
    }
    url = "https://graph.facebook.com/v2.6/%s/" % USER_ID
    r = requests.get(url, params=body)
    #print r.text
    output = json.loads(r.text)
    #recursively go through the dictionary
    my_list = FbGraph.loopDict(output, [])
    return my_list
    
  @staticmethod    
  def all_albums_photos():
    # TASK 3:
      # Step 1. Call my_albums from the previous task to get a list of all my album ids
      # Step 2. Output all captions of every photo for each album id
    body = {
        'access_token': ACCESS_TOKEN,
        'fields' : "albums{photos{name},id}"
    }
    
    url = "https://graph.facebook.com/v2.6/%s/" % USER_ID
    r = requests.get(url, params=body)
    output = json.loads(r.text)

    # create a list of each album ID
    id_list = []
    for one_album in my_list:
        for tup in one_album:
            if 'id' in tup[0]:
                id_list.append(tup[1])

    # collect the albums we are looking for and their photos
    names =FbGraph.get_album_photo(output, [], id_list)
    
    # print out the name of each photo
    for tup in names:
        print "From Album ID: " , tup[1]
        for each_dict in tup[0]:
            FbGraph.print_name(each_dict)
            print
    return



if __name__ == '__main__':
    fb = FbGraph
    #part 1
    #brute force approach to get use to facebook API, datatype
    parse_about = fb.about_me()
    print 'Part: 1'
    for line in parse_about:
        print '\n' + line + ': '
        # parsing a list of dictionaries (language)
        if isinstance(parse_about[line], list):
            for inner in parse_about[line]:
                for k,v  in inner.items(): # a dictionary
                    if 'name' in k and line == 'languages':
                        print v
                    if k == 'school' and line == 'education':
                        for in_k, in_v in v.items():
                            if in_k == 'name':
                                print in_v
        else:
            print parse_about[line]
    
    print '\nPart: 2'
    #print out the text
    my_list = fb.my_albums()
    for one_album in my_list:
        new_list = sorted(one_album, key = lambda tup: tup[0],reverse = True)
        for tup in new_list:
            print tup[0], ": ", tup[1]
        print 

    
    
    print '\nPart: 3' 
    fb.all_albums_photos()
    