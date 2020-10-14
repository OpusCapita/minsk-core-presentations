from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import User
from diagrams.generic.place import Datacenter
from diagrams.onprem.network import Internet
from diagrams.saas.chat import Slack
from diagrams.generic.compute import Rack
from diagrams.generic.device import Mobile

text = "I want: \nOrder: feature-2079\nUser&MD: 2020Q2\nShop: 2020Q2\nQuote: 2020Q2\nInventory: 2020Q2\n..."

with Diagram("\n\nHow it should work", show=False):
  u = User("User interface\n(web app)")
  dc = Rack("Automated\nprocess")
  url = Internet("URL to running\ninstallation\n(public Internet)")
  notify = Mobile("Notification")

  u >> Edge(label=text, color="darkgreen") >> dc >> url >> notify
