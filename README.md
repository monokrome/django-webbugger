django webbugger

A simple django application that can be used to track visitors to your website. Uses
the django content-types framework to allow the most flexible approach possible for
processing tracking information.

In this application, a tracking "beacon" represents a single piece of tracking data. Beacons
can consist of a Target, an Entity, and a Source. Only a Target is required, but
Entity and Source are provided for more elaborate tracking systems.

An "Entity" is a django model that stores information related to an HTTP request in
django. An entity can be any django model and can optionally define a method called
"beacon_update" which will be called and passed the request from the tracking view
prior to redirecting to our target URL.

The "Source" can be any django model. This is useful for storing information regarding
where the traffic came from. For instance, in an affiliate marketing system - you could
use the source attribute of our beacon to reference the affiliate that sent the traffic
to your site.

A "target" represents where to redirect traffic after the Beacon has been created. A
target is simply a model that defines a get_beacon_url method, which should return a URL
to the page that our "entity" will be redirected to after processing a beacon. For
compatibility with other django applications, webbugger checks if get_absolute_url is
defined as an attribute on our target model when get_beacon_url does not exist. If
neither of these methods exist, an HTTP 404 is shown because we have nowhere to direct
traffic to after creating the tracking beacon.

