$ALFRED_DIR = `defaults read com.alfredapp.Alfred alfred.sync.folder`.chomp

puts "Current Alfred Dir: #{$ALFRED_DIR}"

# From http://www.madcowley.com/madcode/2010/12/running-migrations-in-sinatra/
Dir.glob("#{File.dirname(__FILE__)}/tasks/*.rake").each { |r| import r }