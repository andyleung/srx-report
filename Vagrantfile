# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

require "vagrant-host-shell"
require "vagrant-junos"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.define "ndo", primary: true do |ndo|
    ndo.vm.box = "juniper/netdevops-ubuntu1404"
    ndo.vm.hostname = "NetDevOps-SRX-Report"
    ndo.vm.network "private_network",
      ip: "10.16.0.10",
      virtualbox__intnet: "SRX-Report-Internal"
    config.vm.synced_folder "", "/vagrant", disabled: false

    ndo.vm.provider "virtualbox" do |v|
    #  v.gui = true
    #  v.customize ["modifyvm", :id, "--nic1", "hostonly"]
    end
    
    ndo.ssh.shell = 'sh'
    
    ndo.vm.provision "shell" do |s|
      s.path = "scripts/server-setup.sh"
    end

    ndo.vm.network "forwarded_port", guest: 5000, host: 15000

  end
  
  config.vm.define "srx" do |srx|
    srx.vm.box = "juniper/ffp-12.1X47-D10.4"
    srx.vm.hostname = "SRX-Report-SRX01"
    srx.vm.provider "virtualbox" do |v|
      #v.gui = true
    end
    srx.vm.network "private_network",
      ip: "10.16.0.1",
      virtualbox__intnet: "SRX-Report-Internal",
      nic_type: 'virtio'
    
    srx.vm.synced_folder "", "/vagrant", disabled: true

    srx.ssh.username = 'root'
    srx.ssh.shell = 'sh'
    srx.ssh.insert_key = false

    srx.vm.provision "file", source: "scripts/srx-setup.sh", destination: "/tmp/srx-setup.sh"
    srx.vm.provision :host_shell do |host_shell|
      host_shell.inline = 'vagrant ssh srx -c "/usr/sbin/cli -f /tmp/srx-setup.sh"'
    end
  end
end
