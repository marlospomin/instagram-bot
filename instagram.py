#!/usr/bin/env python3

from instapy import InstaPy
from instapy import smart_run
from optparse import OptionParser

# Set usage help text
usage_help_text = "Usage: %prog [options] -u your-account -p your-password [-h]"

# Command line argument parser
parser = OptionParser(usage=usage_help_text)
# Add flags
parser.add_option("-u", "--username", dest="username", default=None, help="Your Instagram username, default=none")
parser.add_option("-p", "--password", dest="password", default=None, help="Your Instagram password, default=none")
parser.add_option("-l", "--private-account", dest="private", action="store_true",
                  default=False, help="Flag whether if your account is private or not, default=false")
parser.add_option("-e", "--extended", dest="extended", action="store_true", default=False,
                  help="Flag if you want to follow more and unfollow everyone afterwards, default=false")
parser.add_option("-a", "--accounts", dest="amount_of_accounts", default=10, help="Amount of accounts to follow, default=10")
# Parse and initialize arguments
(options, args) = parser.parse_args()

# Add parser required arguments or throw an error
if (options.username == None or options.password == None):
    parser.error("Missing username and/or password arguments")

# Store default credentials
username = options.username
password = options.password

# Flag if your account if private or not
my_account_is_private = options.private
# Flat whether you want extended follows and complete unfollows
extended_options = options.extended
# Number of accounts to be followed for each account gathered
amount_of_accounts_to_follow = options.amount_of_accounts
# Unfollow after X time
unfollow_after = options.amount_of_accounts / 6 * 60 * 60

# Create a new bot instance
session = InstaPy(username=username, password=password, headless_browser=True, disable_image_load=True)

# Main instance
def main():
    # Start a session
    with smart_run(session):
        #
        # Settings
        #
        # Don't unfollow users that contributed to your account somehow (2 to exclude other bots)
        session.set_dont_unfollow_active_users(enabled=True, posts=2)
        # Don't follow dummy accounts and limit private accounts
        session.set_skip_users(skip_private=False, private_percentage=75,
                               skip_no_profile_pic=True, no_profile_pic_percentage=100)
        # Set the target accounts the script should interact with
        session.set_relationship_bounds(enabled=True, potency_ratio=None,
                                        delimit_by_numbers=True, max_followers=7500,
                                        max_following=5000, min_followers=100, min_following=50)
        # Set a custom delay to not get caught by the bot detector
        session.set_action_delays(enabled=True, follow=10, unfollow=7.5, randomize=True, random_range=(25, 125))
        # Set limits for the amount of server calls performed hourly
        session.set_quota_supervisor(enabled=True, peak_server_calls=(200, None), sleep_after=["server_calls_h"], sleepyhead=True)
        #
        # Actions
        #
        # Get accounts you follow (AKA your friends)
        if (not my_account_is_private):
            accounts_to_get_users_from = session.grab_following(username=username, amount=10, live_match=False)
        else:
            # Private accounts aren't supported yet cos of the method above
            print("Private accounts aren't supported at this time!")
            # Exit
            exit(1)
        # Set the amount of unfollows to the total amount of follows
        amount_of_accounts_to_unfollow = len(accounts_to_get_users_from) * amount_of_accounts_to_follow
        # Follow followers of the desired accounts (X each account)
        session.follow_user_followers(accounts_to_get_users_from, amount=amount_of_accounts_to_follow, randomize=True)
        # Accept follow requests if my_account_is_private is True
        if (my_account_is_private):
            session.accept_follow_requests(amount=100, sleep_delay=7.5)
        # Unfollow accounts that didn't follow you back (only accounts interacted by the bot)
        session.unfollow_users(amount=amount_of_accounts_to_unfollow, InstaPyFollowed=(True, ("nonfollowers" if extended_options else "all")),
                               style="RANDOM", unfollow_after=unfollow_after)
        # Check if extended_options is enabled
        if (extended_options):
            # Follow accounts that your friends follow
            session.follow_user_following(accounts_to_get_users_from, amount=(amount_of_accounts_to_follow / 3), randomize=True)
            # Unfollow everyone who the bot followed
            session.unfollow_users(amount=(amount_of_accounts_to_unfollow + (amount_of_accounts_to_follow / 3)), InstaPyFollowed=(True, "all"), style="RANDOM", unfollow_after=(unfollow_after * 2))
        #
        # End
        #

if __name__ == "__main__":
    main()
