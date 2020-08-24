from bs4 import BeautifulSoup
import requests
import smtplib
import sys

# google "my user agent"
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

class MyCoupang:

    def get_urls(self):
        '''(myCoupang) -> (list)
        return list contains URLs from input.txt file
        '''
        f = open("/Users/seankim/Desktop/Sean's file/github/MyCoupang/input.txt", "r")
        url_list = []
        for url in f:
            url_list.append(url.strip())
        f.close()
        return url_list


    def add_url_price(self,url,des_price):
        '''(MyCoupang, str, int) -> None
        write url and desired price into input file
        '''
        f = open("/Users/seankim/Desktop/Sean's file/github/MyCoupang/input.txt", "a")
        title,price = self.url_get_title_price(url)
        content = url.strip() + "<SEP>" + title + "<SEP>" + str(des_price).strip() + "\n"
        # if price >= des_price:
        #     self.send_email(url)
        f.write(content)
        f.close()
        return

    def delete_product(self, title):
        '''(MyCoupang, str) -> bool
        return true iff product info is removed from input file given title
        '''
        
        deleted = False
        f = open("/Users/seankim/Desktop/Sean's file/github/MyCoupang/input.txt", "r")
        lines = f.readlines()
        f.close()

        f = open("/Users/seankim/Desktop/Sean's file/github/MyCoupang/input.txt", "w")
        for line in lines:
            if title != line.split("<SEP>")[1].strip():
                f.write(line)
                deleted = True
            elif title == line.split("<SEP>")[1].strip():
                print("Title:",title,"is removed")
        f.close()
        return deleted
        

    def show_products(self):
        '''(MyCoupang) -> none
        show all products in input file
        '''

        f = open("/Users/seankim/Desktop/Sean's file/github/MyCoupang/input.txt", "r")
        for line in f:
            print("Title:",line.split("<SEP>")[1].strip(),", Desired Price:",line.split("<SEP>")[2].strip())
        f.close()
        return

    def url_get_title_price(self, url):
        '''(MyCoupang, list) -> (str, int)
        return title and price of product given the url
        '''
        # send request given url
        page = requests.get(url, headers=headers)

        # html parse
        soup = BeautifulSoup(page.content, 'html.parser')

        # extract title and real price
        title = soup.find("h2","prod-buy-header__title").get_text()
        price = int(soup.find("strong").get_text()[:-1].replace(',',''))
        
        return title,price

    def send_email(self,url):
        '''(MyCoupang, str) -> None
        send notification email with messgae 
        '''
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        server.ehlo()
        # encript connection
        server.starttls()
        server.ehlo()

        # turn on the 2-step passwords on google and receive app password
        server.login('EXAMPLE@gmail.com', 'EXAMPLE_PASSWORDS')

        subject = 'Price fell down!!'
        body = 'Check Coupang website' + url

        msg = f"Subject: {subject}\n\n{body}"

        # send email(from, to, message)
        server.sendmail(
            'EXAMPLE@gmail.com',
            'EXAMPLE@gmail.com',
            msg
        )
        print('Email has been sent!')

        server.quit()

        return


    def price_check(self):
        '''(MyCoupang) -> None
        Check real-price on website and desired price. 
        Send email iff real-price goes down under the desired price
        '''
        down = False
        url_list = self.get_urls()
        for url in url_list:
            url,des_price = url.split("<SEP>")[0], int(url.split("<SEP>")[2])
            title,real_price = self.url_get_title_price(url)
            if real_price <= des_price:
                print(title, " price fell down")
                down = True
                self.send_email(url)
        if not down:
            print("nothing")
        return


    def _main(self):
        '''(MyCoupang) -> None
        MyCoupang Star protocol
        '''
        print("Welcome to MyCoupang!")
        input_value = None
        while input_value != 3:
            print("----------------------------------------------")
            print("1. Check price of the products already have")
            print("2. Add new product with URL and desired price")
            print("3. Delete product")
            print("4. List of all products you are interested in")
            print("5. Quit")
            print("----------------------------------------------")
            input_value = input("Please type NUMBER to select given option!\n")
            try:
                option = int(input_value)
            except ValueError:
                print("{input} is not a number, please enter a number only".format(input=input_value))
            if option == 1: # CHECK PRICE
                self.price_check()
                print('\n')
            elif option == 2: # ADD NEW PRODUCT
                done = False
                while not done:
                    input_url = input("Please type URL you want to add!\n")
                    des_price = input("Please type desired price!\n")
                    try:
                        des_price = int(des_price)
                    except ValueError:
                        print("{input} is not a number, please enter a number only".format(input=input_value))
                    else:
                        self.add_url_price(input_url,des_price)
                        done = True
                        print("product is added")
                print('\n')
            elif option == 3: # DELETE PRODUCT
                
                self.show_products()
                done = False
                while not done:
                    # deleted is boolean variable
                    input_delete = input("Please type title to remove!\n")
                    deleted = self.delete_product(input_delete)
                    if deleted:
                        done = True
                    else:
                        print("{input} is not existed in product list, please re-enter title".format(input=input_value))
            elif option == 4: # SHOW ALL PRODUCT
                self.show_products()
                print('\n')
            elif option == 5: # QUIT
                print('\n')
                return
            else:
                print("{input} number is not in option, please enter a valid number only".format(input=input_value))

            
if __name__ == "__main__":
    my = MyCoupang()
    my._main()