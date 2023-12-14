from flask import Flask, render_template, request, redirect, url_for, session
import datetime
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'auraa'
 
client = MongoClient('mongodb+srv://sam:sam@aura-event.tcy5jcs.mongodb.net/?retryWrites=true&w=majority')
db = client['college_event']
users_collection = db['users']

db = client['job_portal']
jobs_collection = db['jobs']
users_collection = db['users'] 

# jobs2_collection = db['jobs2']


def fetch_logo_url(job_id):
    # Retrieve the logo URL associated with the job from MongoDB
    job = jobs_collection.find_one({'_id': job_id})
    if job:
        return job.get('logo', '')  # Return the logo URL if it exists in the job data
    return ''


@app.route('/')
def index():
    recent_jobs = jobs_collection.find({}).sort('_id', -1).limit(5)
    random_jobs = jobs_collection.aggregate([{ '$sample': { 'size': 3 } }])

    return render_template('index.html', recent_jobs=recent_jobs, random_jobs=random_jobs)

@app.route('/settings')
def settings():
    return render_template('settings.html')
    
@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/my-resume')
def resume():
    return render_template('my-resume.html')

@app.route('/browse-category')
def bro_category():
    return render_template('browse-categories.html')


@app.route('/manage-application')
def manage_app():
    return render_template('manage-application.html')

@app.route('/browse-jobs')
def bro_jobs():
    jobs = jobs_collection.find({})
    # Convert _id to string in each job document
    # jobs = [{'_id': str(job['_id']), **job} for job in jobs]
    return render_template('browse-jobs.html', jobs=jobs)

@app.route('/job-page')
def jobpage():
    jobs = jobs_collection.find({})
    jobs = [{'_id': str(job['_id']), **job} for job in jobs]
    return render_template('job-page.html', job=jobs)

@app.route('/job/<job_id>')
def job_page(job_id):
    job = jobs_collection.find_one({'_id': ObjectId(job_id)})  # Convert job_id to ObjectId
    return render_template('job-page.html', job=job)


@app.route('/add-job', methods=['GET', 'POST'])
def addjob():
    print(request.form)
    if request.method == 'POST':
        job_gmail = request.form['job_gmail']
        job_type = request.form['job_type']
        job_title = request.form['job_title']
        job_time = request.form['job_time'] 
        job_location = request.form['job_location'] 
        location = request.form['location']
        job_salary = request.form['job_salary']
        # job_description = request.form['job_description']
        # benefits = request.form['benefits']
        # requirements = request.form['requirements']
        company_name = request.form['company_name'] 
        # about_company = request.form['about_company']
        # company_email = request.form['company_email'] 
        # company_number = request.form['company_number']
        company_website = request.form['company_website'] 

        # extra fields
        twitter_name = request.form['twitter_username'] 
        description = request.form['description'] 

        respo1 = request.form['respo1']
        respo2 = request.form['respo2']
        respo3 = request.form['respo3']
        respo4 = request.form['respo4']

        req1 = request.form['req1']
        req2 = request.form['req2']
        req3 = request.form['req3']
        req4 = request.form['req4']

        job_id = request.form.get('job_id')
        logo_url = fetch_logo_url(job_id)

        # data
        job_data = {
            'job_gmail': job_gmail,
            'job_title': job_title,
            'job_type': job_type,
            'job_time': job_time,
            'job_location': job_location,
            'location': location,
            'job_salary': job_salary,
            # 'job_description': job_description,
            # 'benefits': benefits,
            # 'requirements': requirements,
            'company_name': company_name,
            # 'about_company': about_company,
            # 'company_description': company_description,
            'company_website': company_website,
            # 'company_contact': {
            #     'email': company_email,
            #     'number': company_number,
            #     'website': company_website
            # },
            # Additional fields
            'twitter_name': twitter_name,
            'description': description,
            # 'responsibilities': responsibilities,
            # 'job_requirements': job_requirements,

            'respo1': respo1,
            'respo2': respo2,
            'respo3': respo3,
            'respo4': respo4,

            'req1': req1,
            'req2': req2,
            'req3': req3,
            'req4': req4
        }

        if logo_url:
            job_data['logo'] = logo_url  # Assign the fetched logo URL if available


        job_data['added_by'] = session['username']
        jobs_collection.insert_one(job_data)
        return redirect(url_for('index'))

    return render_template('add-job.html')



@app.route('/all_jobs')
def all_jobs():
    # Fetch all jobs from the database
    jobs = jobs_collection.find({})  # Fetch all jobs from MongoDB

    return render_template('jobs.html', jobs=jobs)


@app.route('/manage-job')
def manage_jobs():
    if 'username' in session:
        # Fetch jobs added by the current user
        user_jobs = jobs_collection.find({'added_by': session['username']})

        return render_template('manage-jobs.html', username=session['username'], jobs=user_jobs)
    else:
        return redirect(url_for('login'))
    

@app.route('/delete_job/<job_id>', methods=['POST'])
def delete_job(job_id):
    job_id = ObjectId(job_id)
    deleted_job = jobs_collection.delete_one({'_id': job_id, 'added_by': session['username']})
    if deleted_job.deleted_count == 1:
        # Job deleted
        return redirect(url_for('manage_jobs'))
    else:
        # Job not found 
        return "Job not found or you are not authorized to delete this job."




@app.route('/home')
def home():
    if 'username' in session:
        jobs = list(jobs_collection.find())
        return render_template('home.html', username=session['username'], jobs=jobs)
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Received username: {username}, password: {password}")

        if users_collection.find_one({'username': username}):
            return "Username already exists!"
        else:
            users_collection.insert_one({'username': username, 'password': password})
            print("User registered successfully!")
            return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username, 'password': password})

        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            session['error'] = "Invalid username or password. Please try again."
            return redirect(url_for('login'))

    error = session.pop('error', None)
    return render_template('account.html', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('index'))



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        job_title = request.form['job_title']
        job_location = request.form['job_location']
        job_salary = request.form['job_salary']
        job_description = request.form['job_description']
        benefits = request.form['benefits']
        requirements = request.form['requirements']
        company_name = request.form['company_name']
        about_company = request.form['about_company']
        company_description = request.form['company_description']
        company_email = request.form['company_email']
        company_number = request.form['company_number']
        company_website = request.form['company_website']

        job_data = {
            'job_title': job_title,
            'job_location': job_location,
            'job_salary': job_salary,
            'job_description': job_description,
            'benefits': benefits,
            'requirements': requirements,
            'company_name': company_name,
            'about_company': about_company,
            'company_description': company_description,
            'company_contact': {
                'email': company_email,
                'number': company_number,
                'website': company_website
            }
        }

        job_data['added_by'] = session['username']
        jobs_collection.insert_one(job_data)
        return redirect(url_for('home'))

    return render_template('admin.html')
    


if __name__ == '__main__':
    app.run(debug=True)
