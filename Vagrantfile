# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/contrib-jessie64"
  config.vm.provision "shell" do |s|
    s.path = "resources/provision.sh"
    s.env = { "ACCESS_KEY_ID" => ENV['AWS_ACCESS_KEY_ID'],
              "SECRET_ACCESS_KEY" => ENV['AWS_SECRET_ACCESS_KEY']}
  end

  config.vm.define :loadbalancer do |p|
    p.vm.network "forwarded_port", guest: 80, host: 8080
    p.vm.network "private_network", ip: "172.28.128.4"
    p.vm.hostname = "loadbalancer"
    p.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.name = "loadbalancer"
      vb.cpus = "1"
    end
  end

  config.vm.define :app1 do |m|
    m.vm.network "private_network", ip: "172.28.128.3"
    m.vm.hostname = "app-01"
    m.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.name = "app-01"
      vb.cpus = "1"
    end
  end

  config.vm.define :app2 do |b|
    b.vm.network "private_network", ip: "172.28.128.5"
    b.vm.hostname = "app-02"
    b.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.name = "app-02"
      vb.cpus = "1"
    end
  end
end
