#Affilinet Client

Client for Affilinet Api

## Install

From source

    python setup.py build
    sudo python setup.py install

## Requirements

* suds

## Quickstart

Fetch your programs

    from affilinet.clients import PublisherClient
    client = PublisherClient(username="PublisherId", password="WebServicePassword")

    result = client.get_my_programs()
    print "%d program(s) fetched" % result.TotalRecords
    for prog in result.Programs[0]:
        print "%s (%d)" % (prog.ProgramTitle, prog.ProgramId)


Fetch vouchers

    from affilinet.clients import PublisherClient
    client = PublisherClient(username="PublisherId", password="WebServicePassword")

    result = client.get_voucher_codes()
    for voucher in result.VoucherCodeCollection:
        print voucher

Search creatives

    from affilinet.clients import PublisherClient
    client = PublisherClient(username="PublisherId", password="WebServicePassword")

    result = client.get_my_programs()
    programs = []
    for prog in result.Programs[0]:
        programs.append(prog.ProgramId)

    result = client.search_creatives(program_ids=programs, min_width=300,
            max_width=300, min_height=250, max_height=250, page_size=60)
    for creative in result.CreativeCollection[0]:
        print creative
