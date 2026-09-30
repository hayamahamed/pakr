# Pakr

Unpack and repack `.pak` files while preserving the PAK metadata.

This tool is primarily intended for repacking browser `.pak` files after altering their resources without recompiling the browser core.

```sh
pip install pakr
```

Pakr supports **Chromium PAK versions 4 and 5**.

Pakr does not modify the original `.pak` file directly. Instead, it unpacks the PAK into a directory and creates a new PAK when repacking, helping keep the original file free from corruption.

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

```
pakr unpack example.pak pakr-unpacked
pakr pack pakr-unpacked pakr-packed.pak

cmp -n 12 example.pak pakr-packed.pak
echo $?
```
STDOUT:
```
324 resources, 73 aliases -> pakr-unpacked
wrote pakr-packed.pak
0
```

_A return code of `0` from `cmp -n 12` means that the first 12 bytes of the original and reconstructed PAK are identical._

## Disclosure

The core Python code was developed with AI assistance. Edge cases may be present.

Pakr is primarily intended for browser `.pak` file alteration. Use with other PAK formats or applications is outside the intended scope.

## License

Pakr is licensed under the MIT License. The MIT License is a short, permissive license that allows use, modification, distribution, and sublicensing, subject to preserving the copyright and license notices. SEE [LICENSE](LICENSE).

