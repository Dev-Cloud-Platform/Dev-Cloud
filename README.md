![alt logo](https://raw.githubusercontent.com/Dev-Cloud-Platform/Dev-Cloud/dev/dev_cloud/web_service/assets/app/images/logo-invoice.png)
================

# Python implementation of a Dev Cloud System as aPaaS functionality for Cracow Cloud One System #
    Copyright (C) 2016 Michał Szczygieł     <michal.szczygiel@wp.pl>

    This program is free software: you can redistribute it and_or modify
    it under the terms of the Apache License 2.0.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Apache License 2.0 for more details.

    You should have received a copy of the Apache License 2.0
    along with this program.  If not, see <http://www.apache.org/licenses/LICENSE-2.0>.

### Tickets
[![Stories in Ready](https://badge.waffle.io/Dev-Cloud-Platform/Dev-Cloud.png?label=1%20-%20Ready&title=Ready)](https://waffle.io/Dev-Cloud-Platform/Dev-Cloud) [![Stories in Working](https://badge.waffle.io/Dev-Cloud-Platform/Dev-Cloud.png?label=2%20-%20Working&title=Working)](https://waffle.io/Dev-Cloud-Platform/Dev-Cloud) [![Stories in Testing](https://badge.waffle.io/Dev-Cloud-Platform/Dev-Cloud.png?label=3%20-%20Testing&title=Testing)](https://waffle.io/Dev-Cloud-Platform/Dev-Cloud) 
[![Stories in Done](https://badge.waffle.io/Dev-Cloud-Platform/Dev-Cloud.png?label=4%20-%20Done&title=Done)](https://waffle.io/Dev-Cloud-Platform/Dev-Cloud) 
### Status
[![Build Status](http://192.245.169.169:8111/app/rest/builds/buildType:DevCloud_Build/statusIcon)](http://192.245.169.169:8111/viewType.html?buildTypeId=DevCloud_Build&guest=1)
### Throughput Graph
[![Throughput Graph](https://graphs.waffle.io/dev-cloud-platform/dev-cloud/throughput.svg)](https://waffle.io/dev-cloud-platform/dev-cloud/metrics) 

### About
The project focuses on modern technology which is an application platform as a service.
It allows the user to create defined tools for virtual machines located on the Web. 
These tools are suitable applications which gives possibility to run the software dedicated for specific languages programming. 
The aim was to create a system which offering functionality aPaaS (Application platform as a service) be is in synergy with the system Cracow Cloud One which
gives opportunity to use virtualization and procedures for managing virtual machines.
The scope of the subject of the work was to examine the existing service that would offer similar
the possibility of creating specific tools and final step design the system and implement it.
Work has focused on the proper preparation of Virtual machines at the demand of users, whose task is easy, fast and flexible configuration of the operating environment.
In order to prepare a virtual machine according to user demand and its management mechanisms used contextualization Cracow provided by Cloud One and proprietary solutions based on containers LXC (Linux Containers) to automate the process of creating.
These containers are elements system Linux, which provide system virtualization, allowing commissioning many isolated systems controlled by a host system which is superior.
To create a system was used technologies like Python with the Django framework, Juju, Celery with Redis server, TeamCity server and Apache.
The system beyond the graphical development environment used to control the platform from the browser website also provides an API that allows to manage by HTTP request.

***

### Abstrakt
Projekt  skupia się na nowoczesnej technologii będącej usługą platformy aplikacyjnej.
Temat pracy skupia się na nowoczesnej technologii będącej usługą platformy aplikacyjnej.
Umożliwia ona użytkownikowi utworzenie zdefiniowanych narzędzi na wirtualnych maszynach
znajdujących się w sieci internetowej. Narzędzia te stanowią odpowiednie aplikacje dzięki którym
istnieje możliwość uruchomienia oprogramowania dedykowanego pod konkretne języki
programowania. Celem pracy było utworzenie systemu oferującego funkcjonalność systemu aPaaS
(ang. application Platform as a Service) będącego w synergii z system Cracow Cloud One, który
udostępnił sposobność użycia mechanizmów wirtualizacji oraz procedur do zarządzania
wirtualnymi maszynami.
Do zakresu tematu pracy należało zbadanie istniejących usług, które oferowałyby podobną
możliwość tworzenia zdefiniowanych narzędzi, zaprojektowanie takiego systemu oraz jego
wdrożenie i przetestowanie. Problematyka pracy koncentruje się na odpowiednim przygotowaniu
wirtualnej maszyny pod zapotrzebowania użytkowników, którego zadaniem jest łatwa, szybka
i elastyczna konfiguracja środowiska operacyjnego. W celu przygotowania maszyny wirtualnej
według zapotrzebowania użytkownika i jej zarządzania zastosowano mechanizmy kontekstualizacji
dostarczane przez Cracow Cloud One oraz autorskie rozwiązania bazujące na kontenerach LXC
(ang. Linux Containers) automatyzujących proces tworzenia. Kontenery te są elementami
systemowymi Linuksa, które zapewniają systemową wirtualizację, umożliwiającą uruchomienie
wielu odizolowanych systemów kontrolowanych przez hosta będącego system nadrzędnym.
Do stworzenia systemu posłużyły technologie takie jak Python z frameworkiem Django, Juju,
Celery z użyciem serwera Redis, TeamCity oraz serwer Apacha. 
System poza graficznym środowiskiem służącym do kontrolowania platformy z poziomu przegląrki internetowej 
udostępnia także API, które umożliwia zarządzanie przez żądania HTTP.
