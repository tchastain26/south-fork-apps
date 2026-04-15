- [x]**Step 1 -- Add southforkapps.com to Cloudflare**
- Go to cloudflare.com, log in (or create a free account)
- Click "Add a site," enter `southforkapps.com`, choose the Free plan
- Cloudflare will scan your existing DNS records -- review and confirm they look right
- It'll give you two nameserver addresses (e.g. `xxx.ns.cloudflare.com`)

- [x]**Step 2 -- Update nameservers in Hover**
- Log into hover.com → Your Domains → southforkapps.com → Edit Nameservers
- Replace the current nameservers with the two Cloudflare gave you
- Save. DNS propagation takes anywhere from a few minutes to 24 hours

- [x]**Step 3 -- Deploy to Cloudflare Pages**
- In Cloudflare dashboard → Pages → Create a project → Direct Upload
- Upload the `southforkapps` folder
- Cloudflare gives you a `*.pages.dev` URL -- test it there first
- Then go to Custom Domains and add `southforkapps.com`

- [x]**Step 4 -- Add the blog CNAME in Cloudflare DNS**
- In Cloudflare → southforkapps.com → DNS
- Add a CNAME record: Name = `blog`, Target = your Micro.blog hostname (found in Micro.blog under Account → Domain)

- [x]**Step 5 -- Update Micro.blog**
- In Micro.blog → Account → Domain name
- Change it from `southforkapps.com` to `blog.southforkapps.com`