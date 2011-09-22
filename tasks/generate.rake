# curl -v https://api.github.com/repos/kfdm/alfred/downloads

$JEKYLL_HEADER = <<-EOF
---
layout: main
---
EOF

desc 'Generate simple alfred page'
task :generate do
	require 'net/http'
	require 'net/https'
	require 'openssl'
	require 'json'
	https = Net::HTTP.new('api.github.com', 443)
	https.verify_mode = OpenSSL::SSL::VERIFY_NONE
	https.use_ssl = true
	req = Net::HTTP::Get.new('/repos/kfdm/alfred/downloads')
	result = JSON.parse( https.request(req).body )
	File.open('gh-pages/index.md','w') do |f|
		f << $JEKYLL_HEADER
		result.each do |download|
			f << "## #{download['name']}\n"
			f << "#{download['description']} "
			f << "[Download](#{download['html_url']})\n"
		end
	end
end
