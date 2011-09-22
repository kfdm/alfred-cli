namespace :install do
	Dir.glob('{applescripts,scripts}/*').each do |extension|
		desc "Install #{extension}"
		task extension do |t|
			puts "Attempting to install #{t}"
		end
	end
end