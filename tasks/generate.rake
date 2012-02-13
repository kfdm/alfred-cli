# curl -v https://api.github.com/repos/kfdm/alfred/downloads

require "psych"

$JEKYLL_HEADER = <<-EOF
---
layout: main
section: current
---
EOF

desc 'Generate simple alfred page'
task :generate do
	File.open('gh-pages/index.md','w') do |f|
		f << $JEKYLL_HEADER
		@yaml.each_pair do |type, section|
			section.each_pair do |extension, data|
				@plist_path = "#{$LOCAL_DIR}/extensions/#{type}/#{extension}"
				@download = "#{$download_url}/#{type}/#{extension}.alfredextension"
				@description = `defaults read '#{@plist_path}/info' subtitle`
				@tag = extension.gsub(' ', '_').downcase

				f << "## [\\\{#{type}/#{extension}\\\}][#{@tag}]\n"
				f << "#{@description}"
				f << "[#{@tag}]: #{@download}\n\n"
			end
		end
	end
end
