# django webbugger
#### Brandon R. Stoner <monokrome@monokro.me

# What is this?
Django-Webbugger is a simple application that can be used to track visitors to your website. It uses the django content-types framework to allow the most flexible approach possible for processing tracking information. This allows you to customize what data is tracked in a very flexible way.

## Modes of operation
The main view used for tracking is **webbugger.views.trigger** which normally works in redirect mode, but can optionally be told to work in pixel mode instead.

### Redirect Mode
When in redirect mode, the tracking system uses a given Target class to redirect the client to another page after the tracking is finished. This accomplishes a method of tracking that is transparent to users - depending on your URL schema.

### Pixel Mode
The trigger view also takes a keyword argument with the name of "pixel". When set to True, this argument tells the view to return a 1x1 pixel clear GIF instead of redirecting the user to a new page. With this feature, it is possible to embed tracking URLs directly into pages as invisible image elements. Not only that, but you can make use of any online medium that downloads images by this system.

The pixel method allows you to do more clever things, such as including tracking inside of emails in order to see if someone has viewed an email that you sent them - assuming that they have images enabled in their email client, of course.

## Model structure

For everything tracked, a "Beacon" is created. This beacon represents our tracking data. Beacons can consist of a Target, an Entity, and a Source. Entity and Source are provided for systems that want to track some sort of data affiliated with their page hits. A Target is required when redirecting, but it is unneeded when using pixels for tracking.

### Request Entities
An "Entity" is a django model that stores information related to an HTTP request in django. An entity can be any django model and can optionally define a method called "beacon_update" which will be called and passed the request from the tracking view prior to redirecting to our target URL. This allows you to save data from the request straight into the model very easily.

### Traffic Sources
The "Source" can be any django model. This is useful for storing information regarding where the traffic came from. For instance, in an affiliate marketing system - you could use the source attribute of our beacon to reference the affiliate that sent the traffic to your site.

### Target Destinations
When not being used in pixel mode, a "target" represents where to redirect traffic after the Beacon has been created. A target is simply a model that defines a get_beacon_url method, which should return a URL to the page that our "entity" will be redirected to after processing a beacon. For compatibility with other django applications, webbugger checks if get_absolute_url is defined as an attribute on our target model when get_beacon_url does not exist. If neither of these methods exist, an HTTP 404 is shown because we have nowhere to direct traffic to after creating the tracking beacon.

