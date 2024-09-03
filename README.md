I am creating a customer review that is going to cover the current restraunt that I work at. I am going to be using python to grab data using API keys and sorting it into xls sheets. I will the be using the xls sheet to visualize the data into more engaging and appealing graphs using tableau and sql.

I learned to keep the API key I am using a secret through a .env file which will allow git to ignore the file so that my API key is not exposed on github

I found the PLACE ID for each tumble 22 location by creating a python script called collect_tumble22_place_ids. It finds the PLACE ID by grabbing the address and the name to request for the json file. It then updates the .env to hold the PLACE ID for each location. 

By finding the PLACE ID, I was able to request 5 reviews from the Google PLACE API. I wanted to grab all of the reviews for each location but I realized that Googld Place API restricted the amount of request I could pass as I would need to have access from the buisness owner. After getting the json file, I was able to fetch the reviews and store them into a csv file.

I will now be using the csv file to visualize the data even though its not much. I will be using it as practice.

I finished the tableau data visualization of the customer reviews. If there was more data, I would've been able to provide more practical use for it. Here is the link to the public tableau project: [customer review](https://public.tableau.com/app/profile/kenrich.huynh/viz/Tumble22CustomerReview/Dashboard1)
![Dashboard 1](https://github.com/user-attachments/assets/676a1ff0-b723-499c-989a-85dd214c53b6)
