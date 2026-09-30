# Pakr

Unpack and repack `.pak` files while preserving the **Chromium PAK v4 / v5** header data.

This tool is primarily intended for unpacking, altering, and repacking browser `.pak` files without changing the header data.

```sh
pip install pakr
```

Pakr supports **Chromium PAK versions 4 and 5**.

Pakr does not modify the original `.pak` file directly. Instead, it unpacks the PAK into a directory and creates a new PAK when repacking, keeping the original file untouched.

### Unpacking

Pakr:

* Parses the PAK header, resource index, and alias table.
* Writes each resource's raw bytes to a file named after its resource ID.
* Creates `_meta.json` containing the metadata required to reconstruct the PAK.

### Repacking

Pakr:

* Reads `_meta.json` and the resource files.
* Reconstructs the Chromium PAK V4/V5 header.
* Rebuilds the resource index and alias table.
* Concatenates the resource data one after another in order.
* Writes a new `.pak` file.

### Example

Take any supported `.pak` file and rename it to `example.pak`:

```sh
pakr unpack example.pak pakr-unpacked
pakr pack pakr-unpacked pakr-packed.pak

cmp -n 12 example.pak pakr-packed.pak
echo $?
```

STDOOUT:

```text
324 resources, 73 aliases -> pakr-unpacked
wrote pakr-packed.pak
0
```

*A return code of `0` from `cmp -n 12` means that the first 12 bytes of the original and reconstructed PAK are identical.*

## Disclosure

Pakr is primarily intended for browser `.pak` file alteration. Use with other PAK formats or applications is outside the intended scope.
The core Python code was developed with AI assistance. Edge cases may be present.

## License

Pakr is licensed under the MIT License. The MIT License is a short, permissive license that allows use, modification, distribution, and sublicensing, subject to preserving the copyright and license notices. See [LICENSE](LICENSE).
