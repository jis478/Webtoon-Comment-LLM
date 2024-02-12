import pickle
import time
import os
import tqdm
import pickle
import pandas as pd
import logging
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def parsing(comments_all, title, title_id, ep_num, current_page_num):
    parsed_data = []    
    delete_msg = "This comment has been deleted."

    for comments in tqdm.tqdm(comments_all):
        data = comments.split('\n')
        index = 0
        while index < len(data):        

            # exception
            if len(data[index:]) <= 11: # emoji characters
                break
            if data[index] == delete_msg: # deleted msg
                index = index + 3
                continue
            elif data[index + 3] != 'Report': # msg with only emojis
                index = index + 8
                continue
            
            # extraction
            username = data[index]
            top = True if (data[index + 1].startswith('TOP') & (index < 50)) else False
            comment = data[index + 1][3:] if top else data[index + 1] 
            date = data[index + 2]
            report = data[index + 3]
            reply_index = index + 4
            if data[reply_index] == 'Reply':
                replies = 0
                likes = int(data[reply_index + 4])
                dislikes = int(data[reply_index + 6])
                index = reply_index + 7
            elif data[reply_index] == 'Replies':
                replies = int(data[reply_index + 1])
                likes = int(data[reply_index + 4])
                dislikes = int(data[reply_index + 6])
                index = reply_index + 7

            else:
                logging.info(f"Wrong format...")    
                logging.info(parsed_data, title, title_id, ep_num, current_page_num)    
                logging.info(username, top, comment, date, report, data[reply_index])    
                break

            url = f"https://www.webtoons.com/en/romance/{title}/episode-{ep_num}/viewer?title_no={title_id}&episode_no={ep_num}"

            comment_info = {
                'title' : title,
                'title_id' : title_id,
                'episode' : ep_num,
                'url' : url,
                'Username': username,
                'Top': top,
                'Comment': comment,
                'Date': date,
                'Replies': replies,
                'Like': likes,
                'Dislike': dislikes
            }
            parsed_data.append(comment_info)
    
    df = pd.DataFrame(parsed_data)
    return df


def process_episodes(title, title_id, start_ep, end_ep, save_folder):
    os.makedirs(save_folder, exist_ok=True)
    total_ep_df = pd.DataFrame()

    for ep_num in range(start_ep,end_ep+1):

        logging.info(f"  Processing {title}, episode {ep_num}...")    
        url = f"https://www.webtoons.com/en/romance/{title}/episode-{ep_num}/viewer?title_no={title_id}&episode_no={ep_num}"
        driver.get(url)
        time.sleep(10)

        all_comments = []
        init_page_num = 1
        flag = True
        current_page_num = init_page_num

        while flag:

            logging.info(f"    Crawling page #{current_page_num} in episode {ep_num}.")
            comments = driver.find_elements(By.CSS_SELECTOR, "ul.u_cbox_list")
            for comment in comments:
                comment_text = driver.execute_script('return arguments[0].innerText;', comment)
                all_comments.append(comment_text)     
            try:
                if current_page_num % 10 == 0:            
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.u_cbox_next'))
                    )
                    next_button.click()
                    time.sleep(3)
                current_page_num += 1
                page_number_element = driver.find_element(By.XPATH, f'//span[@class="u_cbox_num_page" and text()={current_page_num}]')
                page_number_element.click()
                time.sleep(3)
            except: 
                logging.info(f"End of page")
                flag = False
                break
   
            file_path = os.path.join(save_folder, f'{title}_{ep_num}.pkl')
        
        with open(file_path, 'wb') as file:
            pickle.dump(all_comments, file)
        logging.info(f"Crawling completed")
        
        single_ep_df = parsing(all_comments, title, title_id, ep_num, current_page_num)    
        total_ep_df = pd.concat([total_ep_df, single_ep_df], ignore_index=True)
        
    driver.quit()  # Close the browser
    total_ep_df.to_pickle(f'{title}_{start_ep}_{end_ep}.pkl')
        


def main():
    parser = argparse.ArgumentParser(description='Web crawling for Webtoon episodes')
    parser.add_argument('--title', type=str, default="lore-olympus", help='title')
    parser.add_argument('--title_id', type=int, default=1320, help='title_id')
    parser.add_argument('--start_ep', type=int, default=1, help='Starting episode number')
    parser.add_argument('--end_ep', type=int, default=10, help='Ending episode number')
    args = parser.parse_args()

    title = args.title
    title_id = args.title_id
    start_ep = args.start_ep
    end_ep = args.end_ep
    save_folder = os.path.join('./crawling_results/', str(title_id))
    os.makedirs(save_folder, exist_ok=True)

    logging.basicConfig(filename=os.path.join(save_folder,f'{title_id}_{start_ep}_{end_ep}.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Start processing for {title} ({str(title_id)}) from episode {str(start_ep)} to {str(end_ep)}...")
    process_episodes(title, title_id, start_ep, end_ep, save_folder)
    logging.info("Episodes processing completed.")


if __name__ == "__main__":

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    main()



    