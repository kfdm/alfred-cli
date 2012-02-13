# Build Alfred Extension metadata
# Ref: http://jdfwarrior.tumblr.com/post/13827518019/extension-updater-support

require "psych"


$YAML = "#{$LOCAL_DIR}/alfred.yml"

@yaml = Psych.load File.new( $YAML ).read

desc "Rebuild meta data"
task :build do |t|
    @yaml.each_pair do |type, section|
        section.each_pair do |extension, data|
            puts "#{extension}.#{type}".bold

            @xml_path = "#{$LOCAL_DIR}/extensions/#{type}/#{extension}/update.xml"
            @appcast = "#{$appcast_url}/#{type}/#{extension}.xml"
            puts "\tPackage Metadata: ".yellow.bold
            puts "\t" + @xml_path
            File.new(@xml_path, mode='w').write <<-EOF.gsub(/^ {16}/, '')
                <?xml version='1.0'?>
                <update>
                    <version>#{data['version']}</version>
                    <url>#{@appcast}</url>
                </update>
            EOF

            @xml_path = "#{$LOCAL_DIR}/gh-pages/appcast/#{type}/#{extension}.xml"
            @download = "#{$download_url}/#{type}/#{extension}.alfredextension"
            FileUtils.makedirs File.dirname @xml_path
            puts "\tPackage Appcast: ".green.bold
            puts "\t"+@xml_path
            File.new(@xml_path, mode='w').write <<-EOF.gsub(/^ {16}/, '')
                <?xml version='1.0'?>
                <update>
                    <version>#{data['version']}</version>
                    <url>#{@download}</url>
                </update>
            EOF

            @zip_path = "#{$LOCAL_DIR}/gh-pages/download/#{type}/#{extension}.alfredextension"
            @ext_path = "#{$LOCAL_DIR}/extensions/#{type}/#{extension}"
            puts "\tPackage Zip: ".magenta.bold
            FileUtils.makedirs File.dirname @zip_path
            @cmd = "zip -jr '#{@zip_path}' '#{@ext_path}'"
            puts @cmd
            puts `#{@cmd}`
            puts
        end
    end
end
