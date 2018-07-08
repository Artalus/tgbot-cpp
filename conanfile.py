
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class TgbotConan(ConanFile):
    name = "tgbot_cpp"
    version = "20180620"

    description = "C++ library for Telegram bot API"
    url = "https://github.com/Artalus/tgbot-cpp"
    homepage = "https://github.com/reo7sp/tgbot-cpp"

    license = "MIT"

    exports = ["LICENSE"]

    exports_sources = ["src/*", "CMakeLists.txt", "include/*"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = { "useCurl": [True, False], "fPIC": [True, False] }
    default_options = "useCurl=True", "fPIC=True"

    bv = "1.65.1"
    requires = (
        "boost_system/%s@bincrafters/stable" % bv,
        "boost_asio/%s@bincrafters/stable" % bv,
        "boost_property_tree/%s@bincrafters/stable" % bv,
        "OpenSSL/[>=1.0,<1.1]@conan/stable",
    )
    requires_opt = { "curl": "libcurl/[>=7.21]@bincrafters/stable" }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_TESTS"] = False
        if self.options.useCurl:
            cmake.definitions["HAVE_CURL"] = True
        cmake.configure()
        return cmake

    def requirements(self):
        if self.options.useCurl:
            self.requires(self.requires_opt["curl"])

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses")
        cmake = self.configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        #include_folder = "include"
        #self.copy(pattern="*", dst="include", src=include_folder)
        #self.copy(pattern="*.dll", dst="bin", keep_path=False)
        #self.copy(pattern="*.lib", dst="lib", keep_path=False)
        #self.copy(pattern="*.a", dst="lib", keep_path=False)
        #self.copy(pattern="*.so*", dst="lib", keep_path=False)
        #self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
