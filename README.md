

<br/>
<div align="center">
<h1 align="center">AWS Smart Classroom</h1>
</div>
Our cloud app will include a smart classroom assistant for educators. This assistant collects videos from the user's classroom, performs face recognition on the collected videos, searches the database for the recognized students, and returns the relevant academic information for each student to the user. 

This app's architecture is depicted in the diagram below:

![visualization](https://github.com/dhanrajbhosale/PaaS-AWS-smart-classroom/blob/59e6354fec99b948900e520f2c4f48c83771dbf5/architecture.png?raw=true)
### Built With
Our application runs on Amazon Lambda, a flexible cloud resource that can be easily scaled up or down as needed to meet demand. Student record is stored in DynamoDB, while videos and final output CSV files are stored in S3. Docker Container Images are stored in ECR. This architecture allows us to leverage the power and scalability of cloud computing, while also providing robust and reliable storage solutions for our users' data

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
