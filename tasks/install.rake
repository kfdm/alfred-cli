require 'colored'
namespace :install do
	$INSTALL_TASKS = []
	desc "Install all extensions"
	task :all do |t|
		puts "Installing all tasks".red
		$INSTALL_TASKS.each do |task|
			Rake::Task["install:#{task}"].invoke
		end
	end
	Dir.glob("#{$LOCAL_DIR}/extensions/*/*").each do |extension|
		@SHORTNAME = extension.gsub("#{$LOCAL_DIR}/extensions/",'')
		$INSTALL_TASKS += [@SHORTNAME]
		desc "Install #{@SHORTNAME}"
		task @SHORTNAME do |t|
			@FOLDER = t.name.gsub("install:", "")
			puts "Attempting to install #{@FOLDER}".green
			@LOCAL =  "#{$LOCAL_DIR}/extensions/#{@FOLDER}"
			@REMOTE = File.dirname "#{$ALFRED_DIR}/extensions/#{@FOLDER}"

			sh "cp -rv '#{@LOCAL}' '#{@REMOTE}'"
		end
	end
end

namespace :import do
	Dir.glob("#{$ALFRED_DIR}/extensions/*/*").each do |extension|
		@SHORTNAME = extension.gsub("#{$ALFRED_DIR}/extensions/",'')
		desc "Import #{@SHORTNAME}"
		task @SHORTNAME do |t|
			@FOLDER = t.name.gsub("import:", "")
			puts "Attempting to import #{@FOLDER}".green
			@LOCAL = File.dirname "#{$LOCAL_DIR}/extensions/#{@FOLDER}"
			@REMOTE = extension

			sh "cp -rv '#{@REMOTE}' '#{@LOCAL}'"
		end
	end
end

desc "Re-import extensions into repository"
task :sync do
	Dir.glob("#{$LOCAL_DIR}/extensions/*/*").each do |extension|
		@SHORTNAME = extension.gsub("#{$LOCAL_DIR}/extensions/",'')
		Rake::Task["import:#{@SHORTNAME}"].invoke
	end
end
