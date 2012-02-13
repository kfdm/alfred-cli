# Build Alfred Extension metadata
# Ref: http://jdfwarrior.tumblr.com/post/13827518019/extension-updater-support

require "psych"


$YAML = "#{$LOCAL_DIR}/alfred.yml"

@yaml = Psych.load File.new( $YAML ).read

desc "Rebuild meta data"
task :build do |t|
    puts "Rebuilding Extension Metadata".yellow.bold
    @yaml.each_pair do |type, section|
        section.each_pair do |extension, data|
            @xml_path = "#{$LOCAL_DIR}/extensions/#{type}/#{extension}/update.xml"
            @appcast = "#{$appcast_url}/#{type}/#{extension}.xml"
            puts "Writing: #{@xml_path}"
            File.new(@xml_path, mode='w').write <<-EOF.gsub(/^ {16}/, '')
                <?xml version='1.0'?>
                <update>
                    <version>#{data['version']}</version>
                    <url>#{@appcast}</url>
                </update>
            EOF
        end
    end

    puts "Rebuilding Updater Metadata".yellow.bold
    @yaml.each_pair do |type, section|
        section.each_pair do |extension, data|
            @xml_path = "#{$LOCAL_DIR}/gh-pages/appcast/#{type}/#{extension}.xml"
            @download = "#{$download_url}/#{type}/#{extension}.alfredextension"
            FileUtils.makedirs File.dirname @xml_path
            puts "Writing: #{@xml_path}"
            File.new(@xml_path, mode='w').write <<-EOF.gsub(/^ {16}/, '')
                <?xml version='1.0'?>
                <update>
                    <version>#{data['version']}</version>
                    <url>#{@download}</url>
                </update>
            EOF
        end
    end
end
