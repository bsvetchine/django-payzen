Testing
=======

1. Install the requirements.

::

    pip install -r test-requirements.txt

2. Find a public interface.

If you want to test django-payzen locally and you don't have a public IP you need to expose your localhost over internet to be able to received the payzen payment response request.

You can use a tool like `ngrok <https://ngrok.com/>`_ . Ngrok will give you a public url from wich you can access to your localhost server.

Then you need either to edit your serveur notifications urls or to specify explicitely the notification url in your payment request (recommended).

3. Launch the testing serveur

You need to specify the liverserveur url to 0.0.0.0 to make the testing serveur visible from the network and specify the port accordingly to your ngrok setup.

::

    python manage.py test django_payzen --liveserver 0.0.0.0:8000
