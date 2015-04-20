#Gamification Server

Gamification-server provides a framework for providing awards/points to users or teams and can be operated either standalone or integrated with other web-based applications. Based on the notion of badges used within other gamification systems, gamification-server also provides a customizable web interface for displaying badges as well as a configurable rules engine to translate actions performed by users into awards. User awards can be exported into an Open Badges Backpack, allowing users to present expertise gained within other social frameworks or applications. The gamification-server is implemented as a django python web service and associated web application.

The GeoQ software was developed at the National Geospatial-Intelligence Agency (NGA) in collaboration with [The MITRE Corporation] (http://www.mitre.org).  The government has "unlimited rights" and is releasing this software to increase the impact of government investments by providing developers with the opportunity to take things in new directions. The software use, modification, and distribution rights are stipulated within the [MIT] (http://choosealicense.com/licenses/mit/) license.  


##Pull Requests
If you'd like to contribute to this project, please make a pull request. We'll review the pull request and discuss the changes. All pull request contributions to this project will be released under the MIT license.  

Software source code previously released under an open source license and then modified by NGA staff is considered a "joint work" (see 17 USC § 101); it is partially copyrighted, partially public domain, and as a whole is protected by the copyrights of the non-government authors and must be released according to the terms of the original open source license.

###In the News
NGA Posts Gamification Software on GitHub, October 2014, [Government Computer News](http://gcn.com/blogs/pulse/2014/10/nga-gamification.aspx)

U.S. government releases open source gamification software, October 2014, [Gamasutra]  (http://www.gamasutra.com/view/news/228324/US_government_releases_open_source_gamification_software.php)

##Screenshots

![List of active and inactive projects](https://cloud.githubusercontent.com/assets/147580/4509340/ad46fc92-4b1e-11e4-860c-8e6f4aa3faab.png)

![A Standard Project with two teams counting points](https://cloud.githubusercontent.com/assets/147580/4508998/d1df7902-4b1a-11e4-96eb-8ccfdafebd79.png)

![Custom Themed project](https://cloud.githubusercontent.com/assets/147580/4509000/d1e819fe-4b1a-11e4-991b-83a9757f6f5c.png)

![Alternate Badge Rendering of same project](https://cloud.githubusercontent.com/assets/147580/4509025/1384017a-4b1b-11e4-87fc-89108ca42cee.png)

![Additional Project Details](https://cloud.githubusercontent.com/assets/147580/4509025/1384017a-4b1b-11e4-87fc-89108ca42cee.png)


##APIs and remote usage

Gamification-server is designed so that other sites can send in "signals" that are parsed through a rules engine and generate points and badges.  Also, other sites and apps can pull in JSON to list badges that a user has. For example, the following shows the GeoQ app that is pulling in a list of badges that the current user has:

![GeoQ showing Badges](https://cloud.githubusercontent.com/assets/147580/4509025/1384017a-4b1b-11e4-87fc-89108ca42cee.png)

You can add the ``static/gamification-server-request.js`` file to any remote app and use the following code to add badges to your page. You will only need to have this one file and set up a proxy to make requests:

```javascript
<script src="/static/gamification-server-request.js"></script>
<script>
    $(document).ready(function() {
        gamification.init({
            server_url:"http://gamification-server.com/",
            project_names:"my_app,overall_game",
            user_name: "{{ request.user.username }}",
            $badge_container: $('#badge-container')
        });
    });
</script>
```

You can also pull a direct list of JSON info about a user in a project via:

        % http://<<server_url>>/users/<<username>>/projects/<<project or projects>>/badges?format=json

example:

        % http://<<server_url>>/users/jayc/projects/geoq,GeoQ_Github/badges?format=json


##Configuration

The ``gamification/settings.py`` file contains installation-specific settings. The Database name/pw and server URLs will need to be configured here.  There is a [Chef Script](https://github.com/jaycrossler/django-gamification-chef-installer) that can be used to automatically build and deploy the server to a cloud virtual machine if you prefer.


###Installation

1. Make sure Python, Virtualenv, and Git are installed

2. Install and setup gamification-server:

        % mkdir -p ~/pyenv
        % virtualenv --no-site-packages ~/pyenv/gamification
        % source ~/pyenv/gamification/bin/activate
        % git clone https://github.com/ngageoint/gamification-server

3. Create the database and sync dependencies and data

        % cd gamification-server
        % pip install paver
        % paver install_dependencies
        % paver createdb
        % paver create_db_user
        % paver sync

4. Build user accounts:

        % python manage.py createsuperuser

9. Start it up!

        % python manage.py runserver


