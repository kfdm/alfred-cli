task :server do
  `killall jekyll`
  `cd gh-pages; screen -S jekyll jekyll --server --auto`
end