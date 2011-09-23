namespace :install do
	Dir.glob('extensions/*/*').each do |extension|
		@SHORTNAME = extension.gsub("extensions/",'')
		desc "Install #{@SHORTNAME}"
		task @SHORTNAME do |t|
			puts "Attempting to install #{t}"
		end
	end
end

namespace :import do
	Dir.glob("#{$ALFRED_DIR}/extensions/*/*").each do |extension|
		@SHORTNAME = extension.gsub("#{$ALFRED_DIR}/extensions/",'')
		desc "Import #{@SHORTNAME}"
		task @SHORTNAME do |t|
			@FOLDER = t.name.gsub("import:", "")
			puts "Attempting to import #{@FOLDER}"
			@LOCAL = File.dirname "#{$LOCAL_DIR}/extensions/#{@FOLDER}"
			@REMOTE = extension

			sh "cp -rv '#{@REMOTE}' '#{@LOCAL}'"
		end
	end
end
