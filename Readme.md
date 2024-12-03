
### Composing
Use a suitable HTML Editor to edit the signature.html. Make appropriate commits.

### Deployment
Currently, there are 3 signatures:
  - Signature
  - Signature (no photo)
  - Signature (Enrico)
To deploy, open [c2-panel](https://emailsignatures365.codetwo.com/), insert
 - Signature as is
 - Signature (no photo) without this line:
	``<td valign="top">{RT}<span style="margin: 0 20px 0 0">{Photo 4}</span>{/RT}</td>``
- Signature (Enrico) with the content of `enrico.html` added after 
```
        <p style="margin: 16px 0; font-size: 12px; font-family: Arial; line-height: 16px">
          <a href="mailto:{E-mail}" style="color: rgb(4, 41, 64); text-decoration-color: blue;">{E-mail}</a>
          {RT}
            <br>
            <a href="tel:{Phone}" style="color: rgb(4, 41, 64); text-decoration-color: blue;">{Phone}</a>
          {/RT}
        </p>
```
``
### Testing
  - Test Email Signatures in
	  - new Outlook
	  - old Outlook
	  - Gmail