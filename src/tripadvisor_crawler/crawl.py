from bs4 import BeautifulSoup
import json, requests, re, time, io

user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }

ta_url = 'http://www.tripadvisor.com'
base_url = 'http://www.tripadvisor.com/Attractions-g60974-Activities-'
location_url = 'Buffalo_New_York.html'

def main():
	activities = []

	url = base_url + location_url

	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')

	# get the lazy loaded image list
	image_list = get_image_list(soup)

	page_count = int(soup.select('.pagination a')[-1].text.strip())
	for page_no in range(page_count):
		page_results = soup.select('#FILTERED_LIST .attraction_element')

		# loop over all elements and extract the useful data
		for result in page_results:
			title = result.select('.property_title a')[0].text.strip().encode("utf-8")

			#use the following link to get the reviews
			review_url = ta_url + result.select('a.photo_link')[0]['href'].encode("utf-8")
			reviews = get_reviews(review_url)

			# get image url
			lazy_load_obj = result.select('.photo_booking a img')
			if lazy_load_obj[0].has_attr('id'):
				lazy_load_id = lazy_load_obj[0]['id']
				image_obj = [x['data'] for x in image_list if x['id'] == lazy_load_id]
				image_url = image_obj[0].encode("utf-8")
			else:
				image_url = 'static/images/generic.jpg'

			#get category
			_category = result.select('.matchedTag')[0].text.strip().encode("utf-8")

			data = {"title": title,"review_url": review_url,"image_url": image_url,"category" : _category,"reviews" : reviews}

			activities.append(data)

		# compute the url for the next page
		next_page = base_url + 'oa' + str((page_no + 1) * 30) + '-' + location_url

		time.sleep(15)
		
		response = requests.get(next_page, headers=headers)
		soup = BeautifulSoup(response.content, 'html.parser')

		# get the lazy loaded image list
		image_list = get_image_list(soup)

	activities = json.dumps(activities)
	return activities
	
def get_image_list(soup):
	# get all the script tags then get the one that contains the line
	# 'var lazyImgs'
	script_tags = soup.find_all('script')
	pattern = re.compile('var\s*?lazyImgs\s*?=\s*?(\[.*?\]);', re.DOTALL)

	for tag in script_tags:
		matches = pattern.search(tag.text)    
		if matches:
			image_list = json.loads(matches.group(1))
			return image_list


def get_reviews(review_url):
	url = review_url
	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.content, 'html.parser')

	result = []
	times = []
	page_count = 0
	if soup.select('.pagination a') == []:
		page_count = 1
	else:
		page_count = int(soup.select('.pagination a')[-1].text.strip())

	print review_url
	print "total review pages: " + str(page_count)
	for page_no in range(page_count):
		print "crawling review page: " + str(page_no+1)
		reviews = soup.find_all("p", "partial_entry")
		for review in reviews:
			string = (review.contents)[0].encode("utf-8")
			string = string.replace("\n", "") 
			if string == "":
				continue
	  		result.append(string)

		# compute the url for the next page
	  	next_url = "Reviews-or" + str((page_no+1)*10)
		url = review_url.replace("Reviews",next_url)
		time.sleep(15)
		response = requests.get(url, headers=headers)
		soup = BeautifulSoup(response.content, 'html.parser')
	
	return result

if __name__ == '__main__':
	f = open("data_" + location_url[:-5] + ".json", "w+")
	activities = main()
	f.write(activities)
	f.close()
