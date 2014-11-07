import settings
from map_utils import gen_path
from cassandra.cluster import Cluster
import sys 

# Create derived variables
print len(sys.argv)
if len(sys.argv) == 2:
    org = str(settings.ORG)
    thing = str(sys.argv[1])
else:
    print "Usage: %s thing_id" % sys.argv[0]
    sys.exit()

print org
print "got here"
