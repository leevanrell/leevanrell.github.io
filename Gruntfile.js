module.exports = function (grunt) {

    var log = function (err, stdout, stderr, cb) {
        if(stdout) {
            grunt.log.writeln(stdout);
        }
        if(stderr) {
            grunt.log.error(stderr);
        }
        cb();
    };

    grunt.initConfig({
        shell: {
            jekyllClean: {
                command: "jekyll clean",
                options: {
                    callback: log
                }
            },
            jekyllBuild: {
                command: "bundle exec jekyll build",
                options: {
                    callback: log
                }
            }
        },
        watch: {
            posts:{
                files:[
                    "_config.yml",
                    "*.html",
                    "*.md",
                    "*.yml",
                    "_layouts/**",
                    "_posts/**",
                    "_drafts/**",
                    "_includes/**",
                    "_data/**",
                    "_sass/**/*.*",
                    "assets/**/*.*",
                    "css/**/*.*"
                ],
                tasks: ["shell:jekyllBuild"]
            },
            pyscripts: {
                files:[
                    "misc/bookmarks.txt",
                    "misc/get_articles.py",
                    "_data/bookmarks.yml"
                ],
                tasks: ["shell:bookmarksBuild"],
                options: {
                    spawn: false
                }
            }
        },
        browserSync: {
            dev: {
                bsFiles: {
                    src : [
                        "_site/**/*.*"
                    ]
                },
                options: {
                    watchTask: true,
                    server: "./_site"
                }
            }
        }
    });

    grunt.event.on("watch", function(action, filepath) {
        grunt.config("file_src", filepath);
    });   

    grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.loadNpmTasks("grunt-shell");
    grunt.loadNpmTasks("grunt-browser-sync");
    grunt.registerTask("default", ["build", "browserSync", "watch"]);
    grunt.registerTask("build",["shell:jekyllBuild"]);
    grunt.registerTask("clean",["shell:jekyllClean"]);
};
