import daemon

from rest import main

with daemon.DaemonContext():
    main()