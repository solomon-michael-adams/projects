Design:

SQL tables: users, sneakers, profile

Users consists of 3 categories that are used. The first is id; this is each user's unique id. Next, is username which is inserted through
registration as long as hash which is the hash of inserted password from registration. Last, is a category called count, which initially
had a purpose. But, I redesigned an aspect of my site and it no longer has use. However when I go to remove it, it says that there is a bug
within the application that does not allow me to delete. Basically, an issue I have no control over, so it is still there though it is irrelevant.

Sneakers holds all necessary information for the sneakers. It assigns each sneaker a unique id then holds the name, description, colorway,
style ID, release date, retail price, image url, and purchase url for each sneaker.

Last is profile. This stores the id for each row, user id, shoe id, and boolean statements for whether or not a specific shoe is in the wishlist,
favorites, or purchased shoes lists. The purpose is to store each users lists for the profile on the index page.

Register:
When you arrive at the site, you will either be prompted to register or to login. If you are new, you will obviously register. Clicking the register
link takes you to the register page which has two methods (get and post). Get simply shoes the register.html template. Post, on the other hand, will
submit the form. The form is 3 input boxes. One requiring a username and the other two requiring matching passwords. The password has requirements.
It requires an uppercase letter, lowercase letter, must be 6 character, must have a number and must have a special character. If you do not meet these
requirements, you will be sent to an apology template that says which change you need to make. The register function when called by post, verifies that
there is in fact an input in all boxes and that the username does not already exist in the sequel database, makes sure that all password requirements are
met and then insert the username and hashed password in the users table for future reference. It also logs you in by storing the current user's id. Once
you meet the criteria, you will be redirected to the index page.
Log In:
To login, you click the Log In link. Here, you insert your username and password and it verifies that the user actually put a value into both boxes.
Then, it checks the users table to see if the username exists and then checks if the corresponding hash matches. After you are logged in by storing the
user's id for this session.

Search:
Search was the first function I implemented. Initially, I planned to utilize an API and call on an existing database. However after several hours in
office hours, multiple TAs could not help me to get them connected because all of the sneaker databases we found were in JavaScript. The only one that
I could've used in StockX. But you have to request it, and it was said that it could take several (3+) weeks to obtain. Therefore, that was too long
because I needed to get started. To solve this, I instead manually added about 50 sneakers to a sneakers table just for the scope of this project.
The search function has to methods (POST and GET). When GET is called, the search template is displayed. On this template, is a search bar in which you
can input a shoe name and search for it. When you input a name, it is then cross referenced with all names in the sneaker SQL table to see if there are
any names like it. Then all results are populated on another template called "searched.html." But, if no results are found then the template
"nonexistent.html" appears; this page essentially prompts you to manually add the shoe to the table. The page says "there are no matching results."
Then, it displays the link to add a shoe which goes to the "/add" route. Nevertheless when results are found, each sneaker is populated as a button
that links to the respective profile for each shoe. The reason they are buttons is to make sure that the post method is attained via a form where data
can be obtained from the page without using JavaScript. In addition to the image and title of each shoe being populated through Jinja, each button has
the value of the respective shoe's id so it can be used in the shoe.html template. The shoe.html template is basically a card for each sneaker with
basic information; all the information for the shoe that is stored in the sneakers table and is displayed for the user. The name, description,
colorway, release date, price, style, image url, and purchase url are all pulled from the sneakers table based on which sneaker you click on based
on the corresponding sneaker id that is stored in the shoe, purchase it, or add it to their favorites, wishlist, or purchased lists. The link to purchase is a button
that redirects you to stockX's site for that shoe, should you choose to buy it. As mentioned, at the very bottom, there is a form where you
can add it to whichever list(s) -- favorites, wishlist, purchased -- you choose. When you submit this form (assuming the user selected at least one
of the options), the shoe id, the user id are inserted into the chart. To validate which options are chosen, the checkboxes return None if
unselected, so I check all the checkboxes. If they return None, I set that variables value to false and insert that value in place. Otherwise, the
checkbox has the value true when selected and that is inserted into the table for that specific shoe and that specific user when the form is submitted.
The track which list the shoe is in, there are three categories in the profile table titled top, wishlist, and purchased respectively. Each one is a
boolean, either true meaning that the corresponding shoe id is in the list for the corresponding user id. Basically, it confirms which list for
which user each shoe that is added corresponds to, if you will. After, you are redirect to the index to see your additions added to your list(s) and
displayed in your profile.

Add:
To compensate for the fact that there is no API connection, I instead created the add feature. This allows the user to manually add a sneaker to
database, as long as they have all the necessary information, which is all available on StockX (the API that I would've used, if possible). It is
just a form that when submit POSTs to the index, but prior to inserts all elements into a row in the sneakers table. Now, when this sneaker is searched
for, it will populate with the appropriate results. It also will have its own sneaker profile and thus can be added to the user's profile via the form at
the bottom of the shoe.html template.
Index/Profile:
Index is the most important page but contains the least amount of code. It basically just pulls all shoes that are in the wishlist, favorites, and
purchased lists. It does this by creating three lists with all the info for sneakers from sneakers where wishlist in profile is true, where favorites
in profile is true, or where purchased in profile is true. These three lists each correspond to what their titles imply the favorites list, wishlist,
and purchased list. These lists are then passed on to the index template, and populated using for loops in Jinja. You may also notice that on the index,
there is the edit link. This link sends you to a form should you want to remove anything from one of your lists displayed on your profile. It is a
template of checkboxes populated with jinja based on the profiles table via GET. For POST, for loops are used to see which checkboxes are checked and
then changing the corresponding boolean for wishlist, favorites, or purchased to false. It then redirects to index which is updated via other functions
that have been explained.
Settings:
Settings is just a very simple page where there are two links that go to forms to do simple SQL actions. First, is the delete accounts function.
Basically, this takes you to a template via GET, this template is form that confirms the user wants to delete their account. If the user says yes,
then their information is removed from the users table. Then, they are redirect to index, which requires a login so they will be prompted to log in
or register. Next is the change password function. When you click on the link it takes you to a page that is very similar to the registration page.
It is a form where you input the password. It redirects to the same apology pages if there is no password is provided, the passwords don't match, or
if it doesn't meet the password requirements. Once all requirements are met the input replaces the current hash in the users table for the
current user via session["user_id"]. Then, it redirects to "/logout" requiring you to log back in with your new password.

* I decided to use buttons as the sneaker images because any other method that I could think of would require that I use JavaScript to store values
and utilize functions that I am unfamiliar with to pass information from one Jinja template to the next. But by utilizing the POST and GET capabilities
along with forms (such as buttons), I was able to request.form.get all data that I needed. *
