require 'colored'

$ALFRED_DIR = `defaults read com.alfredapp.Alfred alfred.sync.folder`.chomp
$LOCAL_DIR = File.dirname(__FILE__)

$appcast_url = 'http://kfdm.github.com/alfred/appcast'
$download_url = 'http://kfdm.github.com/alfred/downloads'
$image_url = 'http://kfdm.github.com/alfred/images'

print "Current Alfred Dir :  ".green.bold
puts $ALFRED_DIR

print "Current Working Dir : ".green.bold
puts $LOCAL_DIR

# From http://www.madcowley.com/madcode/2010/12/running-migrations-in-sinatra/
Dir.glob("#{$LOCAL_DIR}/tasks/*.rake").each { |r| import r }