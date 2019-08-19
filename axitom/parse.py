def parse_xtekct_file(file_path):
    """Parse a X-tec-CT file into a dictionary
    Only = is considered valid separators

        Parameters
        ----------
        file_path : string
            The path to the file to be parsed

        Returns
        -------
        string
            A dictionary containing all key-value pairs found in the X-tec-CT input file
        """
    myvars = {}
    with open(file_path) as myfile:
        for line in myfile:
            name, var = line.partition("=")[::2]
            try:
                if "." in var:
                    myvars[name.strip()] = float(var)
                else:
                    myvars[name.strip()] = int(var)
            except ValueError:
                myvars[name.strip()] = var

    return myvars